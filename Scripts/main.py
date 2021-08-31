# Developed By Jonathon Everatt

# Import modules
from matplotlib.pyplot import waitforbuttonpress
from numpy import double
import numpy

# Import my classes
import SimilarityMeasures
import importData
import genImages
import DataCalculations

image_point_count = 0
Image_scale_array = []

def Run_File(filename):
    
    ################################## Import Data
    
    # testPointSet = importData.importGeoJSonAsPoints('Test36507.geojson')
    if filename.find('.txt') != -1:
        print('Running for for idealised data')
        PointSet = importData.importIdealisedData(filename)
    elif filename.find('geo') != -1: # GeoJSON file
        somevar = ''
        threshold = 0.6
        while somevar == '':
            print('Importing Real World Data')
            PolygonSet = importData.importGeoJSonAsPolygons("Data/RealWorldData/" + str(filename), threshold)  
            importData.displayPolygonSet(PolygonSet)
            PointSet = importData.convertPolygonsToCentroids(PolygonSet) 
            somevar = input('Lower the threshold?(Enter) Continue?(Press any key)')
            threshold -= 0.05
    else: 
        exit()
        
    DataCalculations.normaliseData(PointSet)
        
    # global image_point_count
    # image_point_count = len(PointSet)
    # # while image_point_count**2 < len(PointSet):
    # #     image_point_count += 1
    # # image_point_count = (image_point_count - 1)**2 + (len(PointSet) - (image_point_count-1)**2)
    # # print(image_point_count)
    # print('The data has been imported into the program')
    # ################################## Rotation and Scale
    
    # print("Calculating the rotation")
    # Image_rotation_array = DataCalculations.calcImageRotation(PointSet)
    # print("Calculating the Scale")
    # global Image_scale_array
    # Image_scale_array = DataCalculations.CalcScale(PointSet)

    # print('Rotation and Scale Calculations completed. Continue?')
    # waitforbuttonpress()
    # ################################## Generate Images
    # genImages.genImageIdealised(PointSet)

    # print("The Source Image has been generated")
    # print()
    # double_rectangle_count = genImages.genAllTemplate(Image_scale_array)
    # image_count = len(Image_scale_array)

    # ################################## Load Images into array at different scales
    # source_image = importData.loadImageFromFile('MainImage.png', False, 0)
 
    # template_image_square_list = importData.loadImageFromFile('TemplateSquare', False, image_count)
    # template_image_rectangle_list = importData.loadImageFromFile('TemplateRectangle', False, double_rectangle_count)
    # template_image_isosceles_triangle_list = importData.loadImageFromFile('TemplateTriangle', False, image_count)
    # template_image_quincunx_list = importData.loadImageFromFile('TemplateQuincunx', False, image_count)
    # template_image_equilateral_triangle_list = importData.loadImageFromFile('TemplateEquilateralTriangle', False, image_count)
    # template_image_double_hedgerow_list = importData.loadImageFromFile('TemplateDoubleHedge', False, double_rectangle_count)
    # print("Source image and Templates loaded")
    # print()
    
    # ################################## Template Matching
    
    # for rotation in Image_rotation_array: # Testing each template at each possible rotation
    #     correlation_threshold = 0.6
    #     evaluation_array = []
    #     while correlation_threshold < 1:
    #         print()
    #         print()
    #         print("Correlation threshold set to: " + str(round(correlation_threshold,2)))
    #         print('Testing templates at a rotation of ' + str(rotation))

    #         for x in range(len(template_image_square_list)):
    #             count = SimilarityMeasures.templateMatching_correlation(source_image, template_image_square_list[x], correlation_threshold)
    #             if count > (0.5 * image_point_count):
    #                 evaluation_array.append([count, numpy.round(correlation_threshold,1), x, 'Square'])
                
    #         for x in range(len(template_image_rectangle_list)):
    #             count = SimilarityMeasures.templateMatching_correlation(source_image, template_image_rectangle_list[x], correlation_threshold)
    #             if count > (0.5 * image_point_count):
    #                 evaluation_array.append([count, numpy.round(correlation_threshold,1), int(numpy.round(x/len(Image_scale_array))), 'Rectangle'])
                
    #         for x in range(len(template_image_isosceles_triangle_list)):
    #             count = SimilarityMeasures.templateMatching_correlation(source_image, template_image_isosceles_triangle_list[x], correlation_threshold)
    #             if count > (0.5 * image_point_count):
    #                 evaluation_array.append([count, numpy.round(correlation_threshold,1), x, 'Isosceles Triangle'])
            
    #         for x in range(len(template_image_quincunx_list)):
    #             count = SimilarityMeasures.templateMatching_correlation(source_image, template_image_quincunx_list[x], correlation_threshold)
    #             if count > (0.5 * image_point_count):
    #                 evaluation_array.append([count, numpy.round(correlation_threshold,1), x, 'Quincunx'])
                
    #         for x in range(len(template_image_equilateral_triangle_list)):
    #             count = SimilarityMeasures.templateMatching_correlation(source_image, template_image_equilateral_triangle_list[x], correlation_threshold)
    #             if count > (0.5 * image_point_count):
    #                 evaluation_array.append([count, numpy.round(correlation_threshold,1), x, 'Equilateral Triangle'])
                
    #         for x in range(len(template_image_double_hedgerow_list)):
    #             count = SimilarityMeasures.templateMatching_correlation(source_image, template_image_double_hedgerow_list[x], correlation_threshold)
    #             if count > (0.5 * image_point_count):
    #                 evaluation_array.append([count, numpy.round(correlation_threshold,1), int(numpy.round(x/len(Image_scale_array))), 'Double HedgeRow'])
            
    #         correlation_threshold += 0.1
    
    # evaluateData(evaluation_array)
    

def evaluateData(evaluation_array):
    print()
    print()
    for x in range(len(evaluation_array)):
        print(str(evaluation_array[x][0]) + " matches were found at a " + str(evaluation_array[x][1]) + " correlation level")
        print("with a scale of " + str(Image_scale_array[evaluation_array[x][2]]) + " and a planting pattern of " + str(evaluation_array[x][3]))

    
def RunTestCases():
    file_input_name = 'SquareIdeal3.txt'
    print("Square Template")
    
    Run_File(file_input_name)
    print()
    print()
    print("Run for Rectangle?")
    waitforbuttonpress()
    print("Running for rectangle")
    file_input_name = 'RectIdeal3.txt'
    Run_File(file_input_name)
    print()
    print()
    
    print("Run for Triangle?")
    waitforbuttonpress()
    print("Running for Triangle")
    file_input_name = 'TriIdeal3.txt'
    Run_File(file_input_name)
    
    print()
    print()
    print("Run for Quincunx?")
    waitforbuttonpress()
    print("Running for Quincunx")
    file_input_name = 'QuincunxIdeal3.txt'
    Run_File(file_input_name)
    print()
    print()
    
    print("Run for DoubleHedge?")
    waitforbuttonpress()
    print("Running for DoubleHedge")
    file_input_name = 'DoubleHedgeIdeal3.txt'
    Run_File(file_input_name)
    
    print()
    print()
    print("Run for Rectangle?")
    waitforbuttonpress()
    print("Running for rectangle")
    file_input_name = 'RectNoise24.txt'
    Run_File(file_input_name)
    print()
    print()
    
    print("Run for Triangle?")
    waitforbuttonpress()
    print("Running for Triangle")
    file_input_name = 'TriNoise3.txt'
    Run_File(file_input_name)
    
    print()
    print()
    print("Run for Quincunx?")
    waitforbuttonpress()
    print("Running for Quincunx")
    file_input_name = 'QuincunxNoise3.txt'
    Run_File(file_input_name)
    print()
    print()
    
    print("Run for DoubleHedge?")
    waitforbuttonpress()
    print("Running for DoubleHedge")
    file_input_name = 'DoubleHedgeNoise3.txt'
    Run_File(file_input_name)


if __name__ == '__main__':
    print('The program has started.')    
    file_input_name = input("What is the image name(0 for default)?\n")
    if file_input_name == '0':
        file_input_name = 'SquareIdeal3.txt'
        print("Using default")
        print()
        Run_File(file_input_name)
    elif file_input_name == '1':
        RunTestCases()
    elif file_input_name == '2':
        file_input_name = 'square_real.geojson'
        print("Using GeoJSON default")
        print()
        Run_File(file_input_name)
    else:
        Run_File(file_input_name)