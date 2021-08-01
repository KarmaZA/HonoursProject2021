# Developed By Jonathon Everatt


# Import modules
import cv2


# Import my classes
import SimilarityMeasures
import importData

# import numpy as np

# Global Variables
display_image_on_load = False



def loadImageFromFile(file_name):
    print("Loading the image file.")
    image = cv2.imread(file_name, 0)
    if not image.any():
        print("Error image not loaded")

    if flag_check:
        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
        window_show_sized = cv2.resize(image, (960, 540))
        cv2.imshow("Image", window_show_sized)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    print("Image loaded.")
    return image


if __name__ == '__main__':
    print('Testing the importData class')
    testVar = importData.importGeoJSONData('Test36507.geojson')

    print("The program has started.")
    flag_check = input("Do you want to see the image loaded (Y/N)?\n")
    if flag_check == 'Y':
        display_image_on_load = True

    file_input_name = input("What is the image name(0 for default)?\n")
    if file_input_name == '0':
        file_input_name = '695787.png'
        print("Using default")

    source_image = loadImageFromFile(file_input_name)
    print("Image loaded")
    template_image = loadImageFromFile('Template695.png')
    print("Template loaded")
    # SimilarityMeasures.correlation_measure = templateMatching_leastSquares(source_image, template_image)
    SimilarityMeasures.templateMatching_leastSquares(source_image, template_image)
