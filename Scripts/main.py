# Developed By Jonathon Everatt


# Import modules
import cv2


# Import my classes
import SimilarityMeasures
import importData
import genImages
import calcRotation


# Global Variables
display_image_on_load = False



def loadImageFromFile(file_name):
    print("Loading the image file.")
    image = cv2.imread(file_name, 0)
    if not image.any():
        print("Error image not loaded")

    # if display_image_on_load:
    #     cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    #     window_show_sized = cv2.resize(image, (960, 540))
    #     cv2.imshow("Image", window_show_sized)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()
    print("Image loaded.")
    return image


def Run_File(filename):
    
    ################################## Import Data
    # testPointSet = importData.importGeoJSonAsPoints('Test36507.geojson')
    PointSet = importData.importIdealisedData(filename)
    print('The data has been imported into the program')
    ################################## Rotation
    calcRotation.calcImageRotation(PointSet)
    ################################## Generate Images
    
    genImages.genImageIdealised(PointSet)

    print("The Templates haven been generated")
    
    ##################################
    print("The program has started.")
    flag_check = 'Y'#input("Do you want to see the image loaded (Y/N)?\n")
    if flag_check == 'Y':
        display_image_on_load = True
        
    ################################## Load Images
    source_image = loadImageFromFile('MainImage.png')
    print("Image loaded")

    template_image_square = loadImageFromFile('TemplateSquare.png')
    template_image_rectangle = loadImageFromFile('TemplateRectangle.png')
    template_image_triangle = loadImageFromFile('TemplateTriangle.png')
    print("Template loaded")
    
    ################################## Template Matching
    count = SimilarityMeasures.templateMatching_correlation(source_image, template_image_rectangle)
    print("The number of template matches for rectangle template is: " + str(count))
    count = SimilarityMeasures.templateMatching_correlation(source_image, template_image_triangle)
    print("The number of template matches for triangle template is: " + str(count))
    count = SimilarityMeasures.templateMatching_correlation(source_image, template_image_square)
    print("The number of template matches for square template is: " + str(count))
    

def RunTestCases():
    file_input_name = 'SquareIdeal3.txt'
    print("Square Template")
    
    Run_File(file_input_name)
    print()
    print()
    some_val = input("Run for Rectangle?")
    print("Running for rectangle")
    file_input_name = 'RectIdeal3.txt'
    Run_File(file_input_name)
    print()
    print()
    some_val = input("Run for Triangle?")
    
    print("Running for Triangle")
    file_input_name = 'TriIdeal3.txt'
    Run_File(file_input_name)


if __name__ == '__main__':
    print('The program has started.')
    file_input_name = input("What is the image name(0 for default)?\n")
    if file_input_name == '0':
        file_input_name = 'SquareIdeal3.txt'
        print("Using default")
        Run_File(file_input_name)
    elif file_input_name == '1':
        RunTestCases()
    else:
        Run_File(file_input_name)