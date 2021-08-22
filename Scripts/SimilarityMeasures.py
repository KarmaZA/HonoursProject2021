# Developed By Jonathon Everatt
# This file will contain template matching similarity measures for the template matching algorithms

import cv2
import numpy as np

# Template matching using normalized Cross Correlation
def templateMatching_correlation(source_image, template_image, threshold):
    source_image_gray = source_image
    res = cv2.matchTemplate(source_image_gray, template_image, cv2.TM_CCOEFF_NORMED)
    
    loc = np.where( res >= threshold)
    count = 0
    for pt in zip(*loc[::-1]):
        #cv2.rectangle(source_image_gray, pt, (pt[0] + width, pt[1] + height), (128,128,128), 2)
        count += 1
    return count