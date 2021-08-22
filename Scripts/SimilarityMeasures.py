# Developed By Jonathon Everatt
# This file will contain template matching similarity measures for the template matching algorithms

from PIL.Image import NONE
import cv2
from matplotlib import pyplot as plt
import numpy as np
from shapely.geometry.point import Point

# Template matching using normalized Cross Correlation
def templateMatching_correlation(source_image, template_image, threshold):
    #height, width = template_image.shape[::-1]
    
    source_image_gray = source_image#cv2.cvtColor(source_image, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(source_image_gray, template_image, cv2.TM_CCOEFF_NORMED)
    
    loc = np.where( res >= threshold)
    count = 0
    for pt in zip(*loc[::-1]):
        # print(res)
        #cv2.rectangle(source_image_gray, pt, (pt[0] + width, pt[1] + height), (128,128,128), 2)
        count += 1
    return count

# Template matching using normalized Cross Correlation
def templateMatching_correlation_score(source_image, template_image):
    #height, width = template_image.shape[::-1]
    
    source_image_gray = source_image#cv2.cvtColor(source_image, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(source_image_gray, template_image, cv2.TM_CCOEFF_NORMED)
    threshold = 0.99

    loc = np.where(result > threshold)
    #Stopgap solution fix
    while len(loc[0]) == 0:
        threshold -= 0.01
        loc = np.where(result > threshold)
    
    # Round to 2 decimal point for easier use. Can be extended but unlikely to be useful beyond 2 due to noise
    return round(threshold,2)

    