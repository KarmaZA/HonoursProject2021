# Developed By Jonathon Everatt
# Import my classes

import os
import time
import cv2
import imutils

from sklearn.neighbors import KDTree

import TemplateMatch
import importData
import genImages
import DataCalculations
import DataOutput
import ParameterCalculations
import EvaluateData

Image_scale_array = []


def Run_File(filename):
    RWdata = False
################################################# Step 1 ###################################################################################
############################################ Import Data ###################################################################################
    if filename.find('.txt') != -1:
        # print('Running for for idealised data')
        PointSet = importData.importIdealisedData(filename)
    elif filename.find('geo') != -1: # GeoJSON file
        somevar = ''
        threshold = 0.4
        RWdata = True
        # while somevar == '':
            # print('Loading GeoJSON file')
        PointSet = importData.importGeoJSonAsPoints("Data/RealWorldData/" + str(filename), threshold)  
            # importData.displayPolygonSet(PolygonSet)
            # PointSet = importData.convertPolygonsToCentroids(PolygonSet) 
            # somevar = ' a'#input('Lower the threshold?(Enter) Continue?(Press any key)')
            # threshold -= 0.05
    else: 
        exit()
    print("Data loaded")

    # import matplotlib.pyplot as plt
    # xs = [point.x for point in PointSet]
    # ys = [point.y for point in PointSet]
    # plt.gca().set_aspect('equal')
    # plt.scatter(xs,ys, color = 'black')
    # # plt.axis('off') # So the image only has points
    # print(len(PointSet))
    # plt.show()
 
###################################################### Functions to calc parameters and TM problem values #############################################
    dataset = KDTree(PointSet)
    source_image_number = DataCalculations.GenerateSubImages(PointSet)
    # print(source_image_number)

    PointSet, average_angle, tree_per_row = DataCalculations.rowDetection(PointSet, dataset)
    angle_to_out = DataCalculations.getCommonAngle(average_angle)
    row_count, inter_spacing, road_count = ParameterCalculations.countRowNumbers(PointSet, int(angle_to_out), dataset)
    TreeCoords = ParameterCalculations.CornerTreeCoords(PointSet)
    scale_intra_row = ParameterCalculations.calcScaleIntra(PointSet, dataset)

    # test1, test2 = ParameterCalculations.calcScaleInter(PointSet, angle_to_out)
    # print("is it worth it")
    # print(inter_spacing, test1)
    # print(angle_to_out, test2)
####################################################### Send extracted parameters to output object ###########################################
    Data_out = DataOutput.DataOut()
    
    # Row Rotation
    Data_out.setAngle(angle_to_out)
    #Tree Count
    Data_out.setTreeCount(len(PointSet))
    # Road or ditch count
    Data_out.setRoadCount(road_count)
    #Spacing
    if RWdata:
        coords1= (0,0)
        coords2 = (inter_spacing, 0)
        import geopy.distance
        inter_spacing = geopy.distance.geodesic(coords1, coords2).m
        coords2 = (scale_intra_row, 0)
        scale_intra_row = geopy.distance.geodesic(coords1, coords2).m
    Data_out.setIntra(scale_intra_row)   
    Data_out.setInter(inter_spacing)
    # Number of Rows
    Data_out.setRowNumbers(row_count)
    # Number of Trees per Row
    Data_out.setTreesPerRow(tree_per_row)
    # Coordinates of corner Tree
    Data_out.setCorner(TreeCoords)
    print("Finished parameter extraction")
# ################################################# Step 2 #########################################################################################
    square_score, rectangle_score, equitri_score, isostri_score, quincunx_score, dblhdg_score = (0,0,0,0,0,0)
    squareL, rectangleL, equitri, isostri, quincunxL, dblhdg = ([],[],[],[],[],[])
    flag = False
    image_scale_array = []
    image_count = 1
    double_rectangle_count = 1
    evaluation_array = []
 
#     ################################################# Generate Images ################################################################################
    for x in range(source_image_number):
        source_image = importData.loadImageFromFile('Images/MainImage' + str(x) + '.png', 0)
        source_image = TemplateMatch.cleanTheGraph(source_image) 
        
        source_image = imutils.rotate(source_image, angle=(abs(angle_to_out)-90))
        # cv2.imshow('test', source_image)
        # print(angle_to_out)
        # cv2.waitKey(0)

        image_scale_intra, image_scale_inter = TemplateMatch.CalcScale(source_image)
         

        
        for scales in image_scale_intra:
            if not(scales in image_scale_array):
                image_scale_array.append(scales)
        for scales in image_scale_inter:
            if not(scales in image_scale_array):
                image_scale_array.append(scales)
        if len(image_scale_inter) == 0 or len(image_scale_intra) == 0:
            pass
        if len(image_scale_intra) < 1:
            image_scale_intra = image_scale_inter 
        if len(image_scale_inter) < 1:
            image_scale_inter = image_scale_intra 
        double_rectangle_count = genImages.genAllTemplate(image_scale_intra, image_scale_inter, image_scale_array)
        image_count = len(image_scale_array)
        # print(image_count)
        # print(image_scale_array)

################################################# Load Images into array at different scales #####################################################

        template_image_square_list = importData.loadImageFromFile('TemplateSquare', image_count)
        template_image_rectangle_list = importData.loadImageFromFile('TemplateRectangle', double_rectangle_count)
        template_image_isosceles_triangle_list = importData.loadImageFromFile('TemplateTriangle', double_rectangle_count)
        template_image_quincunx_list = importData.loadImageFromFile('TemplateQuincunx', image_count)
        template_image_equilateral_triangle_list = importData.loadImageFromFile('TemplateEquilateralTriangle', image_count)
        template_image_double_hedgerow_list = importData.loadImageFromFile('TemplateDoubleHedge', double_rectangle_count)
    
################################################ Template Matching ################################################################################
        

        for x in range(len(template_image_square_list)):
            # print(x)
            count = TemplateMatch.templateMatching_correlation(source_image, template_image_square_list[x])
            square_score, flag = EvaluateData.scoreMatches(count, square_score)
            if flag:
                flag = False
                squareL = count

        for x in range(len(template_image_rectangle_list)):
            # print(x)
            count = TemplateMatch.templateMatching_correlation(source_image, template_image_rectangle_list[x])
            rectangle_score, flag = EvaluateData.scoreMatches(count, rectangle_score)
            if flag:
                flag = False
                rectangleL = count
            # if rectangle_score > 152700:
            #     TemplateMatch.templateMatching_display(source_image, template_image_rectangle_list[x])

        for x in range(len(template_image_isosceles_triangle_list)):
            # print(len(template_image_isosceles_triangle_list))
            count = TemplateMatch.templateMatching_correlation(source_image, template_image_isosceles_triangle_list[x])
            isostri_score, flag = EvaluateData.scoreMatches(count, isostri_score)
            if flag:
                flag = False
                isostri = count

        for x in range(len(template_image_equilateral_triangle_list)):
            count = TemplateMatch.templateMatching_correlation(source_image, template_image_equilateral_triangle_list[x])
            equitri_score, flag = EvaluateData.scoreMatches(count, equitri_score)
            if flag:
                flag = False
                equitri = count

        for x in range(len(template_image_double_hedgerow_list)):
            count = TemplateMatch.templateMatching_correlation(source_image, template_image_double_hedgerow_list[x])
            dblhdg_score, flag = EvaluateData.scoreMatches(count, dblhdg_score)
            if flag:
                flag = False
                dblhdg = count

        for x in range(len(template_image_quincunx_list)):
            count = TemplateMatch.templateMatching_correlation(source_image, template_image_quincunx_list[x])
            quincunx_score, flag = EvaluateData.scoreMatches(count, quincunx_score)
            if flag:
                flag = False
                quincunxL = count

##################################################### Step 3 ###################################################################################
##### Penalise scores
    if inter_spacing > (1.7 * scale_intra_row):
        square_score *= 0.5
        quincunx_score *= 0.5
        # print("Square penalty")
    else:
        # print("Rect pantly")
        rectangle_score *= 0.5
        dblhdg_score *= 0.5


#####Evaluation methods
    pattern_out_array = [square_score, rectangle_score, isostri_score, equitri_score, quincunx_score, dblhdg_score]
    # print(pattern_out_array)
    pattern_out = EvaluateData.Evaluate(pattern_out_array)
    # print(pattern_out)
    Data_out.setPatterns(pattern_out)
##### Write data to output object
    outFileName = filename.split('.')[0]
    if outFileName.find('/') > -1:
        outFileName = outFileName.split('/')[-2]
    Data_out.writeDataToFile(outFileName)

#################################################### Memory Clean Up ##########################################################################
    for x in range(double_rectangle_count):
        if x < source_image_number:
            os.remove('Images/MainImage' + str(x) + '.png')
        if x < image_count:
            os.remove('Images/TemplateSquare' + str(x) + '.png')
            os.remove('Images/TemplateEquilateralTriangle' + str(x) + '.png')
            os.remove('Images/TemplateQuincunx' + str(x) + '.png')
            os.remove('Images/TemplateTriangle' + str(x) + '.png')
        os.remove('Images/TemplateRectangle' + str(x) + '.png')
        os.remove('Images/TemplateDoubleHedge' + str(x) + '.png')
    if(source_image_number > double_rectangle_count):
        for x in range(double_rectangle_count, source_image_number,1):
            if x < source_image_number:
                os.remove('Images/MainImage' + str(x) + '.png')

#################################################### Completed ################################################################################

    print("The program has completed running")
    print("The most likely pattern is " + str(pattern_out_array[0]))
    print("See " + str(outFileName) + ".txt for more information")
    with open("TM" + str(outFileName), 'w') as f:
        f.write(str(pattern_out_array) + '\n')
        f.write('Square ' + str(square_score) + ' ' + str(squareL) + '\n')
        f.write('Rectangle ' + str(rectangle_score) + ' ' + str(rectangleL)  + '\n')
        f.write('Isos ' + str(isostri_score) + ' ' + str(isostri)  + '\n')
        f.write('Equi ' + str(equitri_score) + ' ' + str(equitri)  + '\n')
        f.write('Quin ' + str(quincunx_score) + ' ' + str(quincunxL)  + '\n')
        f.write('Dbl ' + str(dblhdg_score) + ' ' + str(dblhdg)  + '\n')

    
def RunTestCases():
    file_input_name = 'TestIdealData/SquareIdeal3.txt'
    print("Square Template")
    
    Run_File(file_input_name)
    print()
    print()
    print("Run for Rectangle?")
    print("Running for rectangle")
    file_input_name = 'TestIdealData/RectIdeal3.txt'
    Run_File(file_input_name)
    print()
    print()
    
    print("Run for Triangle?")
    print("Running for Triangle")
    file_input_name = 'TestIdealData/TriIdeal3.txt'
    Run_File(file_input_name)
    
    print()
    print()
    print("Run for Quincunx?")
    print("Running for Quincunx")
    file_input_name = 'TestIdealData/QuincunxIdeal3.txt'
    Run_File(file_input_name)
    print()
    print()
    
    print("Run for DoubleHedge?")
    print("Running for DoubleHedge")
    file_input_name = 'TestIdealData/DoubleHedgeIdeal3.txt'
    Run_File(file_input_name)
    
    print()
    print()
    print("Run for Rectangle?")
    print("Running for rectangle")
    file_input_name = 'TestIdealData/RectNoise24.txt'
    Run_File(file_input_name)
    print()
    print()
    
    print("Run for Triangle?")
    print("Running for Triangle")
    file_input_name = 'TestIdealData/TriNoise3.txt'
    Run_File(file_input_name)
    
    print()
    print()
    print("Run for Quincunx?")
    print("Running for Quincunx")
    file_input_name = 'TestIdealData/QuincunxNoise3.txt'
    Run_File(file_input_name)
    print()
    print()
    
    print("Run for DoubleHedge?")
    print("Running for DoubleHedge")
    file_input_name = 'TestIdealData/DoubleHedgeNoise3.txt'
    Run_File(file_input_name)


def IdealisedExp():
    timeArray = []
    try:
        start_time = time.time()
        file_input_name = 'SquareIdeal.txt'
        Run_File(file_input_name)
        timeArray.append(time.time() - start_time)
    except:
        print("SquareIdeal Fail")

    try:
        start_time = time.time()
        file_input_name = 'RectIdeal.txt'
        Run_File(file_input_name)
        timeArray.append(time.time() - start_time)
    except:
        print("SquaRectIdealre Fail")

    try:
        start_time = time.time()
        file_input_name = 'HexagonalIdeal.txt'
        Run_File(file_input_name)
        timeArray.append(time.time() - start_time)
    except:
        print("HexagonalIdeal Fail")

    try:
        start_time = time.time()
        file_input_name = 'IsoscelesIdeal.txt'
        Run_File(file_input_name)
        timeArray.append(time.time() - start_time)
    except:
        print("IsoscelesIdeal Fail")

    try:
        start_time = time.time()
        file_input_name = 'QuincunxIdeal.txt'
        Run_File(file_input_name)
        timeArray.append(time.time() - start_time)
    except:
        print("QuincunxIdeal Fail")

    try:
        start_time = time.time()
        file_input_name = 'DoubleRowIdeal.txt'
        Run_File(file_input_name)
        timeArray.append(time.time() - start_time)
    except:
        print("DoubleRowIdeal Fail")

    print("Time array")
    print(timeArray)
    with open("performance.txt", 'w') as f:
        f.write(str(timeArray))   


def runGeoJSON():    
    timeArray = []
    try:
        start_time = time.time()
        file_input_name = '32377/raw-detections.geojson'
        Run_File(file_input_name)
        timeArray.append(time.time() - start_time)
    except:
        print("32377 Fail")

    try:
        start_time = time.time()
        file_input_name = '35516/raw_detections.geojson'
        Run_File(file_input_name)
        timeArray.append(time.time() - start_time)
    except:
        print("35516 Fail")

    try:
        start_time = time.time()
        file_input_name = '36502/detections_raw.geojson'
        Run_File(file_input_name)
        timeArray.append(time.time() - start_time)
    except:
        print("36502 Fail")

    try:
        start_time = time.time()
        file_input_name = '36507/raw_detections.geojson'
        Run_File(file_input_name)
        timeArray.append(time.time() - start_time)
    except:
        print("36507 Fail")

    try:
        start_time = time.time()
        file_input_name = '36513/detections_raw.geojson'
        Run_File(file_input_name)
        timeArray.append(time.time() - start_time)
    except:
        print("36513 Fail")

    try:
        start_time = time.time()
        file_input_name = '41630/detections_raw.geojson'
        Run_File(file_input_name)
        timeArray.append(time.time() - start_time)
    except:
        print("41630 Fail")

    try:
        start_time = time.time()
        file_input_name = '43581/detections_raw.geojson'
        Run_File(file_input_name)
        timeArray.append(time.time() - start_time)
    except:
        print("43581 Fail")

    print("Time array")
    print(timeArray)
    with open("performance.txt", 'w') as f:
        f.write(str(timeArray)) 
             

def addNoise(filename):
    import random
    count = 0
    with open("Data/IdealData/" + filename) as dataFile:
        with open("Data/" + filename, 'w') as f:
        # point_set = []
            for line in dataFile:
                count = random.randint(0,10)
                coords = line.split()
                x = float(coords[0])
                y = float(coords[1])
                y*= 2
                # if count == 6:
                #     x += (random.randint(-10,10)/10)
                #     print(x)
                # elif count == 7:
                #     y += (random.randint(-10,10)/10)
                #     print(y)
                # point_set.append(Point(x,y))            
                f.write(str(x) + ' ' + str(y) + '\n')


if __name__ == '__main__':
    # addNoise('IsoscelesIdeal.txt')

    print('The program has started.')   
    file_input_name = input("What is the image name(0 for default)?\n")
    start_time = time.time()
    if file_input_name == '0':
        file_input_name = 'DoubleRowIdeal.txt'
        print("Using default")
        print()
        Run_File(file_input_name)
    elif file_input_name == '1':
        IdealisedExp()
    elif file_input_name == '2':
        file_input_name = 'square_real.geojson'
        print("Using GeoJSON default")
        print()
        Run_File(file_input_name)
    elif file_input_name == '3':
        runGeoJSON()
    else:
        Run_File(file_input_name)
    print("--- %s seconds ---" % (time.time() - start_time))