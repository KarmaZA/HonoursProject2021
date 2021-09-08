# Developed By Jonathon Everatt
# This file will contain template matching similarity measures for the template matching algorithms

import cv2
import imageio
import numpy as np
from shapely.geometry import Point, MultiPoint

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


#Calc Scale will return an array of mean distances. These could number from 1 to several
def CalcScale(image):
    min_pixel_value = 0
    PointSet = []
    width, height  = image.shape
    image_centroid_array = []
    for x in range(width):
        pixel_count_array = []
        for y in range(height):
            if image[x][y] == min_pixel_value:
                pixel_count_array.append(y)
            else:
                if len(pixel_count_array) > 0:
                    count = 0
                    for z in pixel_count_array:
                        count += z
                    image_centroid_array.append(x)
                    image_centroid_array.append(int(count/len(pixel_count_array)))
                
    image_centroid_array = np.ndarray(image_centroid_array).reshape(len(image_centroid_array)/2, 2)
    print(image_centroid_array)
            
            
                    
    
    return []
    