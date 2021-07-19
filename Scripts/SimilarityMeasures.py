# Developed By Jonathon Everatt
# This file will contain template matching similarity measures for the template matching algorithms

import cv2
from matplotlib import pyplot as plt

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

    cv2.namedWindow("Matched image", cv2.WINDOW_NORMAL)
    window_show_sized = cv2.resize(source_image, (960, 540));
    cv2.imshow("Matched image", window_show_sized)
    cv2.waitKey()
    cv2.destroyAllWindows()