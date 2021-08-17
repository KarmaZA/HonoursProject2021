# Developed By Jonathon Everatt
# This file will contain template matching similarity measures for the template matching algorithms

from PIL.Image import NONE
import cv2
from matplotlib import pyplot as plt
import numpy as np
from shapely.geometry.point import Point

# Template matching using normalized Cross Correlation
def templateMatching_correlation(source_image, template_image):
    height, width = template_image.shape[::-1]
    
    source_image_gray = source_image#cv2.cvtColor(source_image, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(source_image_gray, template_image, cv2.TM_CCOEFF_NORMED)
    threshold = 0.85
    
    loc = np.where( res >= threshold)
    # print(loc)
    count = 0
    for pt in zip(*loc[::-1]):
        # print(res)
        cv2.rectangle(source_image_gray, pt, (pt[0] + width, pt[1] + height), (128,128,128), 2)
        count += 1
        
    
    plt.imshow(res, cmap='gray')
    
    window_show_sized = cv2.resize(source_image_gray, (960, 540));
    cv2.imshow("Matched image", window_show_sized)
    cv2.waitKey()
    cv2.destroyAllWindows()
    #source_image_gray = None
    return count


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

    cv2.namedWindow("Matched image", cv2.WINDOW_NORMAL)
    window_show_sized = cv2.resize(source_image, (960, 540));
    cv2.imshow("Matched image", window_show_sized)
    cv2.waitKey()
    cv2.destroyAllWindows()

    