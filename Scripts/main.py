# Developed By Jonathon Everatt


# Import modules
import cv2
from matplotlib.pyplot import waitforbuttonpress


# Import my classes
import SimilarityMeasures
import importData
import genImages
import DataCalculations


# Global Variables
display_image_on_load = False


def Run_File(filename):
    
    ################################## Import Data
    # testPointSet = importData.importGeoJSonAsPoints('Test36507.geojson')
    PointSet = importData.importIdealisedData(filename)
    print('The data has been imported into the program')
    ################################## Rotation and Scale
    print("Calculating the rotation")
    # Image_rotation_array = DataCalculations.calcImageRotation(PointSet)
    print("Calculating the Scale")
    # Image_scale_array = DataCalculations.CalcScale(PointSet)
    Image_scale_array = [2, 4, 6, 8, 10]
    ################################## Generate Images
    genImages.genImageIdealised(PointSet)

    print("The Source Image has been generated")
    print()
    
        
    genImages.genAllTemplate(Image_scale_array)
    
    
    # Write code to fix rotatin if necessary
    
    ##################################
    print("The program has started.")
    flag_check = 'N'#input("Do you want to see the image loaded (Y/N)?\n")
    if flag_check == 'Y':
        display_image_on_load = True
        
        
    ################################## Load Images into array at different scales
    source_image = importData.loadImageFromFile('MainImage.png', False)

    # template_image_square = importData.loadImageFromFile('TemplateSquare.png', False)
    # template_image_rectangle = importData.loadImageFromFile('TemplateRectangle.png', False)
    # template_image_isosceles_triangle = importData.loadImageFromFile('TemplateTriangle.png', False)
    # template_image_quincunx = importData.loadImageFromFile('TemplateQuincunx.png', False)
    # template_image_equilateral_triangle = importData.loadImageFromFile('TemplateEquilateralTriangle.png', False)
    # template_image_double_hedgerow = importData.loadImageFromFile('TemplateDoubleHedge.png', False)
    # print("Source image and Templates loaded")
    # print()
    
    # ################################## Template Matching
    # correlation_threshold = 0.1
    # max_count = 0
    # pattern = ''
    # while correlation_threshold < 1:
    #     print()
    #     print()
    #     print("Correlation threshold set to: " + str(round(correlation_threshold,2)))
        
    #     count = SimilarityMeasures.templateMatching_correlation(source_image, template_image_rectangle, correlation_threshold)
    #     print("The number of template matches for rectangle template is: " + str(count))
    #     if count > max_count:
    #         pattern = 'Rectangle'
    #         max_count = count
        
    #     count = SimilarityMeasures.templateMatching_correlation(source_image, template_image_isosceles_triangle, correlation_threshold)
    #     print("The number of template matches for triangle template is: " + str(count))
    #     if count > max_count:
    #         pattern = 'Isosceles triangle'
    #         max_count = count
    #     elif count == max_count:
    #         pattern = pattern + ' and Isosceles triangle'
            
    #     count = SimilarityMeasures.templateMatching_correlation(source_image, template_image_square, correlation_threshold)
    #     print("The number of template matches for square template is: " + str(count))
    #     if count > max_count:
    #         pattern = 'Square'
    #         max_count = count
    #     elif count == max_count:
    #         pattern = pattern + ' and Square'
            
    #     count = SimilarityMeasures.templateMatching_correlation(source_image, template_image_quincunx, correlation_threshold)
    #     print("The number of template matches for quincunx template is: " + str(count))
    #     if count > max_count:
    #         pattern = 'Quincunx'
    #         max_count = count
    #     elif count == max_count:
    #         pattern = pattern + ' and Quincunx'
            
    #     count = SimilarityMeasures.templateMatching_correlation(source_image, template_image_equilateral_triangle, correlation_threshold)
    #     print("The number of template matches for hexangonal/equilateral triangle template is: " + str(count))
    #     if count > max_count:
    #         pattern = 'Equilateral Triangle'
    #         max_count = count
    #     elif count == max_count:
    #         pattern = pattern + ' and Equilateral Triangle'
            
    #     count = SimilarityMeasures.templateMatching_correlation(source_image, template_image_double_hedgerow, correlation_threshold)
    #     print("The number of template matches for double hedgerow template is: " + str(count))
    #     if count > max_count:
    #         pattern = 'Double Hedgerow'
    #         max_count = count
    #     elif count == max_count:
    #         pattern = pattern + ' and Double Hedgerow'
            
    #     print("The planting pattern detected is: " + pattern + ' at a correlation threshold of ' + str(round(correlation_threshold,2)))
    #     print("There were " + str(max_count) + " matches") 
        
    #     max_count = 0
    #     pattern = ''
    #     correlation_threshold += 0.1
    

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


if __name__ == '__main__':
    print('The program has started.')    
    file_input_name = input("What is the image name(0 for default)?\n")
    if file_input_name == '0':
        file_input_name = 'QuincunxIdeal3.txt'
        print("Using default")
        print()
        Run_File(file_input_name)
    elif file_input_name == '1':
        RunTestCases()
    else:
        Run_File(file_input_name)