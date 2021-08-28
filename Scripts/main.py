# Developed By Jonathon Everatt

# Import modules
from matplotlib.pyplot import waitforbuttonpress
from numpy import double

# Import my classes
import SimilarityMeasures
import importData
import genImages
import DataCalculations

def Run_File(filename):
    
    ################################## Import Data
    
    # testPointSet = importData.importGeoJSonAsPoints('Test36507.geojson')
    PointSet = importData.importIdealisedData(filename)
    print('The data has been imported into the program')
    ################################## Rotation and Scale
    
    print("Calculating the rotation")
    Image_rotation_array = DataCalculations.calcImageRotation(PointSet)
    print("Calculating the Scale")
    Image_scale_array = DataCalculations.CalcScale(PointSet)
    somevar = input('Rotation and Scale Calculations completed. Continue?')
    ################################## Generate Images
    genImages.genImageIdealised(PointSet)

    print("The Source Image has been generated")
    print()
    double_rectangle_count = genImages.genAllTemplate(Image_scale_array)
    image_count = len(Image_scale_array)
 
    ################################## Load Images into array at different scales
    source_image = importData.loadImageFromFile('MainImage.png', False, 0)

    template_image_square_list = importData.loadImageFromFile('TemplateSquare', False, image_count)
    template_image_rectangle_list = importData.loadImageFromFile('TemplateRectangle', False, double_rectangle_count)
    template_image_isosceles_triangle_list = importData.loadImageFromFile('TemplateTriangle', False, image_count)
    template_image_quincunx_list = importData.loadImageFromFile('TemplateQuincunx', False, image_count)
    template_image_equilateral_triangle_list = importData.loadImageFromFile('TemplateEquilateralTriangle', False, image_count)
    template_image_double_hedgerow_list = importData.loadImageFromFile('TemplateDoubleHedge', False, double_rectangle_count)
    print("Source image and Templates loaded")
    print()
    
    ################################## Template Matching
    
    for rotation in Image_rotation_array: # Testing each template at each possible rotation
        correlation_threshold = 0.1
        max_count = 0
        pattern = ''
        while correlation_threshold < 1:
            print()
            print()
            print("Correlation threshold set to: " + str(round(correlation_threshold,2)))
            print('Testing templates at a rotation of ' + str(rotation))
            
            for template_image_square in template_image_square_list:
                count = SimilarityMeasures.templateMatching_correlation(source_image, template_image_square, correlation_threshold)
                if count != 0:
                    print("The number of template matches for square template is: " + str(count))
                if count > max_count:
                    pattern = 'Square'
                    max_count = count
                elif count == max_count:
                    pattern = pattern + ' and Square'
                
            for template_image_rectangle in template_image_rectangle_list:    
                count = SimilarityMeasures.templateMatching_correlation(source_image, template_image_rectangle, correlation_threshold)
                if count != 0:
                    print("The number of template matches for rectangle template is: " + str(count))
                if count > max_count:
                    pattern = 'Rectangle'
                    max_count = count
            
            for template_image_isosceles_triangle in template_image_isosceles_triangle_list:
                if count != 0:
                    count = SimilarityMeasures.templateMatching_correlation(source_image, template_image_isosceles_triangle, correlation_threshold)
                if count != 0:
                    print("The number of template matches for triangle template is: " + str(count))
                if count > max_count:
                    pattern = 'Isosceles triangle'
                    max_count = count
                elif count == max_count:
                    pattern = pattern + ' and Isosceles triangle'
                
        
            for template_image_quincunx in template_image_quincunx_list:        
                count = SimilarityMeasures.templateMatching_correlation(source_image, template_image_quincunx, correlation_threshold)
                if count != 0:
                    print("The number of template matches for quincunx template is: " + str(count))
                if count > max_count:
                    pattern = 'Quincunx'
                    max_count = count
                elif count == max_count:
                    pattern = pattern + ' and Quincunx'
                
            
            for template_image_equilateral_triangle in template_image_equilateral_triangle_list:
                count = SimilarityMeasures.templateMatching_correlation(source_image, template_image_equilateral_triangle, correlation_threshold)
                if count != 0:
                    print("The number of template matches for hexangonal/equilateral triangle template is: " + str(count))
                if count > max_count:
                    pattern = 'Equilateral Triangle'
                    max_count = count
                elif count == max_count:
                    pattern = pattern + ' and Equilateral Triangle'
           
            for template_image_double_hedgerow in template_image_double_hedgerow_list:    
                count = SimilarityMeasures.templateMatching_correlation(source_image, template_image_double_hedgerow, correlation_threshold)
                if count != 0:
                    print("The number of template matches for double hedgerow template is: " + str(count))
                if count > max_count:
                    pattern = 'Double Hedgerow'
                    max_count = count
                elif count == max_count & pattern.find('Double') == -1:
                    pattern = pattern + ' and Double Hedgerow'
                
            print("The planting pattern detected is: " + pattern + ' at a correlation threshold of ' + str(round(correlation_threshold,2)))
            print("There were " + str(max_count) + " matches") 
            
            max_count = 0
            pattern = ''
            correlation_threshold += 0.1
    
#
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
        file_input_name = 'QuincunxNoise3.txt'
        print("Using default")
        print()
        Run_File(file_input_name)
    elif file_input_name == '1':
        RunTestCases()
    else:
        Run_File(file_input_name)