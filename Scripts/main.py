# Developed By Jonathon Everatt
# Import my classes

import os
from sklearn.neighbors import KDTree

import TemplateMatch
import importData
import genImages
import DataCalculations
import DataOutput
import ParameterCalculations

Image_scale_array = []


def Run_File(filename):
################################################# Step 1 ###################################################################################
    ############################################ Import Data ###################################################################################
    if filename.find('.txt') != -1:
        print('Running for for idealised data')
        PointSet = importData.importIdealisedData(filename)
    elif filename.find('geo') != -1: # GeoJSON file
        somevar = ''
        threshold = 0.6
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
    # # Graphing test
    # import matplotlib.pyplot as plt
    # xs = [point.x for point in PointSet]
    # ys = [point.y for point in PointSet]
    # plt.gca().set_aspect('equal')
    # plt.scatter(xs,ys, color = 'black')
    # plt.show()
    ###################################################### Functions to calc parameters and TM stuff #############################################
    dataset = KDTree(PointSet)
    #Returns number of images to perform template matching on   
    source_image_number = DataCalculations.GenerateSubImages(PointSet)
    # print(source_image_number)
    print("Sub images generated")
    #Normalise rows into lines
    PointSet, average_angle = DataCalculations.normaliseData(PointSet, dataset)
    print("Rotation has been detected")
    
    angle_to_out = DataCalculations.calcWeightedAverageAngle(average_angle)
    print("Calculated average angle:")
    print(angle_to_out)

    row_count, inter_spacing, road_count = ParameterCalculations.countRowNumbers(PointSet, int(angle_to_out), dataset)
    print("Calculated Row data")

    TreeCoords = ParameterCalculations.CornerTreeCoords(PointSet)
    scale_intra_row = ParameterCalculations.calcScaleIntra(PointSet, dataset)
    ####################################################### Send extracted parameters to output object ###########################################
    Data_out = DataOutput.DataOut()
    
    #Intra-row spacing
    Data_out.setIntra(scale_intra_row)
    # Row Rotation
    Data_out.setAngle(angle_to_out)
    #Tree Count
    Data_out.setTreeCount(len(PointSet))
    # Road or ditch count
    Data_out.setRoadCount(road_count)
    #Inter-row spacing
    Data_out.setInter(inter_spacing)
    # Number of Rows
    Data_out.setRowNumbers(row_count)
    # Number of Trees per Row
    # Data_out.setTreesPerRow()
    # Coordinates of corner Tree
    Data_out.setCorner(TreeCoords)
    print("Finished parameter extraction")
################################################# Step 2 #########################################################################################
    for x in range(source_image_number):
        image_scale_array = [] 
################################################# Generate Images ################################################################################
        source_image = importData.loadImageFromFile('Images/MainImage' + str(x) + '.png', 0)        
        image_scale_array = TemplateMatch.CalcScale(source_image)       

        print("The Source Image has been generated")
        print()
        double_rectangle_count = genImages.genAllTemplate(image_scale_array)
        image_count = len(image_scale_array)

################################################# Load Images into array at different scales #####################################################
 
        template_image_square_list = importData.loadImageFromFile('TemplateSquare', image_count)
        template_image_rectangle_list = importData.loadImageFromFile('TemplateRectangle', double_rectangle_count)
        template_image_isosceles_triangle_list = importData.loadImageFromFile('TemplateTriangle', image_count)
        template_image_quincunx_list = importData.loadImageFromFile('TemplateQuincunx', image_count)
        template_image_equilateral_triangle_list = importData.loadImageFromFile('TemplateEquilateralTriangle', image_count)
        template_image_double_hedgerow_list = importData.loadImageFromFile('TemplateDoubleHedge', double_rectangle_count)
        print("Source image and Templates loaded")
        print()
    
################################################ Template Matching ################################################################################
        
        # for rotation in Image_rotation_array: # Testing each template at each possible rotation
        #     correlation_threshold = 0.6
        #     evaluation_array = []
        #     while correlation_threshold < 1:
        #         print()
        #         print()
        #         print("Correlation threshold set to: " + str(round(correlation_threshold,2)))
        #         print('Testing templates at a rotation of ' + str(rotation))

        #         for x in range(len(template_image_square_list)):
        #             count = TemplateMatch.templateMatching_correlation(source_image, template_image_square_list[x], correlation_threshold)
        #             if count > (0.5 * image_point_count):
        #                 evaluation_array.append([count, numpy.round(correlation_threshold,1), x, 'Square'])
                    
        #         for x in range(len(template_image_rectangle_list)):
        #             count = TemplateMatch.templateMatching_correlation(source_image, template_image_rectangle_list[x], correlation_threshold)
        #             if count > (0.5 * image_point_count):
        #                 evaluation_array.append([count, numpy.round(correlation_threshold,1), int(numpy.round(x/len(Image_scale_array))), 'Rectangle'])
                    
        #         for x in range(len(template_image_isosceles_triangle_list)):
        #             count = TemplateMatch.templateMatching_correlation(source_image, template_image_isosceles_triangle_list[x], correlation_threshold)
        #             if count > (0.5 * image_point_count):
        #                 evaluation_array.append([count, numpy.round(correlation_threshold,1), x, 'Isosceles Triangle'])
                
        #         for x in range(len(template_image_quincunx_list)):
        #             count = TemplateMatch.templateMatching_correlation(source_image, template_image_quincunx_list[x], correlation_threshold)
        #             if count > (0.5 * image_point_count):
        #                 evaluation_array.append([count, numpy.round(correlation_threshold,1), x, 'Quincunx'])
                    
        #         for x in range(len(template_image_equilateral_triangle_list)):
        #             count = TemplateMatch.templateMatching_correlation(source_image, template_image_equilateral_triangle_list[x], correlation_threshold)
        #             if count > (0.5 * image_point_count):
        #                 evaluation_array.append([count, numpy.round(correlation_threshold,1), x, 'Equilateral Triangle'])
                    
        #         for x in range(len(template_image_double_hedgerow_list)):
        #             count = TemplateMatch.templateMatching_correlation(source_image, template_image_double_hedgerow_list[x], correlation_threshold)
        #             if count > (0.5 * image_point_count):
        #                 evaluation_array.append([count, numpy.round(correlation_threshold,1), int(numpy.round(x/len(Image_scale_array))), 'Double HedgeRow'])
                
        #         correlation_threshold += 0.1
        
##################################################### Step 3 ###################################################################################

#   Send data for evaluation

#####Evaluation methods
    # pattern_out_array = []
    # Data_out.setPatterns(pattern_out_array)
#####
    outFileName = filename.split('.')[0]
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
    # print("The most likely pattern is " + str(pattern_out_array[0]))
    print("See " + str(outFileName) + ".txt for more information")

    
def RunTestCases():
    file_input_name = 'TestIdealData/SquareIdeal3.txt'
    print("Square Template")
    
    Run_File(file_input_name)
    print()
    print()
    print("Run for Rectangle?")
    # waitforbuttonpress()
    print("Running for rectangle")
    file_input_name = 'TestIdealData/RectIdeal3.txt'
    Run_File(file_input_name)
    print()
    print()
    
    print("Run for Triangle?")
    # waitforbuttonpress()
    print("Running for Triangle")
    file_input_name = 'TestIdealData/TriIdeal3.txt'
    Run_File(file_input_name)
    
    print()
    print()
    print("Run for Quincunx?")
    # waitforbuttonpress()
    print("Running for Quincunx")
    file_input_name = 'TestIdealData/QuincunxIdeal3.txt'
    Run_File(file_input_name)
    print()
    print()
    
    print("Run for DoubleHedge?")
    # waitforbuttonpress()
    print("Running for DoubleHedge")
    file_input_name = 'TestIdealData/DoubleHedgeIdeal3.txt'
    Run_File(file_input_name)
    
    print()
    print()
    print("Run for Rectangle?")
    # waitforbuttonpress()
    print("Running for rectangle")
    file_input_name = 'TestIdealData/RectNoise24.txt'
    Run_File(file_input_name)
    print()
    print()
    
    print("Run for Triangle?")
    # waitforbuttonpress()
    print("Running for Triangle")
    file_input_name = 'TestIdealData/TriNoise3.txt'
    Run_File(file_input_name)
    
    print()
    print()
    print("Run for Quincunx?")
    # waitforbuttonpress()
    print("Running for Quincunx")
    file_input_name = 'TestIdealData/QuincunxNoise3.txt'
    Run_File(file_input_name)
    print()
    print()
    
    print("Run for DoubleHedge?")
    # waitforbuttonpress()
    print("Running for DoubleHedge")
    file_input_name = 'TestIdealData/DoubleHedgeNoise3.txt'
    Run_File(file_input_name)


if __name__ == '__main__':
    count = array_len = [3,6]
    genImages.genAllTemplate(array_len)
    # source_image = importData.loadImageFromFile('Images/MainImage0.png', 0)    
    # template_image_square_list = importData.loadImageFromFile('TemplateSquare', 1)
    # count = TemplateMatch.templateMatching_correlation(source_image, template_image_square_list[x], correlation_threshold)
    # print(count)

    # print('The program has started.')   
    # file_input_name = input("What is the image name(0 for default)?\n")
    # if file_input_name == '0':
    #     file_input_name = 'TestIdealData/SquareIdeal3.txt'
    #     print("Using default")
    #     print()
    #     Run_File(file_input_name)
    # elif file_input_name == '1':
    #     RunTestCases()
    # elif file_input_name == '2':
    #     file_input_name = 'square_real.geojson'
    #     print("Using GeoJSON default")
    #     print()
    #     Run_File(file_input_name)
    # else:
    #     Run_File(file_input_name)