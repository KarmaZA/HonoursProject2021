# Developed By Jonathon Everatt

import numpy #Import Numpt
import cv2 #Import OpenCV
display_image_on_load = False


def main():
    print("First function called.")


def loadImageFromFile():
    print("Loading the image file.")
    source_image = cv2.imread('695787.png', 1)
    if not source_image.any():
        print("Error image not loaded")

    cv2.imshow('image', source_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("Image loaded.")



if __name__ == '__main__':
    print("The program has started.")

    flagCheck = input("Do you want to see the image loaded (Y/N)?\n0")
    if flagCheck == 'Y':
        display_image_on_load = True

    loadImageFromFile()
    main()
