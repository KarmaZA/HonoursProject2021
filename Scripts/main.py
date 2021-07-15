# Developed By Jonathon Everatt

# Import Numpy
import numpy as np
# Import OpenCV
import cv2
# Matplotlib
from matplotlib import pyplot as plt

display_image_on_load = False


# Template matching using normalized Cross Correlation
def templateMatching_correlation(source_image, template_image):
    print("First function called.")
    correlation = 1
    return correlation


# Template matching using least squares
def templateMatching_leastSquares(source_image, template_image):
    print("First function called.")
    height, width = template_image.shape[::]
    res = cv2.matchTemplate(source_image, template_image, cv2.TM_SQDIFF)
    plt.imshow(res, cmap='gray')

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = min_loc  # Change to max_loc for all except for TM_SQDIFF
    bottom_right = (top_left[0] + width, top_left[1] + height)
    cv2.rectangle(source_image, top_left, bottom_right, (255, 0, 0), 2)

    cv2.imshow("Matched image", source_image)
    cv2.waitKey()
    cv2.destroyAllWindows()


def loadImageFromFile(file_name):
    print("Loading the image file.")
    image = cv2.imread(file_name, 1)
    if not image.any():
        print("Error image not loaded")

    if flag_check:
        cv2.imshow('image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    print("Image loaded.")
    return image


if __name__ == '__main__':
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
    #correlation_measure = templateMatching_leastSquares(source_image, template_image)
    templateMatching_leastSquares(source_image, template_image)
