# Developed By Jonathon Everatt
# This file will contain template matching similarity measures for the template matching algorithms

import cv2
import numpy as np
from shapely.geometry import Point, MultiPoint
import imageio

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
    width, height  = image.shape    
    image_scale_array = []    
    image_scale_y = []
    
    ## Vertical Search
    for x in range(width):
        pixel_array = []
        for y in range(height):
            if image[x][y] == min_pixel_value:
                # We are on a black pixel
                if image[x][y+1] != min_pixel_value:
                    pixel_array.append(y)        
        for z in range(len(pixel_array)-1):
            scalar_difference = pixel_array[z+1] - pixel_array[z]
            if not scalar_difference in image_scale_y:
                image_scale_y.append(int(scalar_difference))       
          
    # image_scale_array = image_scale_array.sort()  
    image_scale_y.sort(key=sortFunc)    
    for count in range(len(image_scale_y)):
        if image_scale_y[count] < int(1.5 *image_scale_y[0]):
            if not image_scale_y[count] in image_scale_array:
                image_scale_array.append(image_scale_y[count])      
                
################### Horizontal search 
    
    image_scale_y = []
    for y in range(height):
        pixel_array = []
        for x in range(width):
            if image[x][y] == min_pixel_value:
                # We are on a black pixel
                if image[x][y+1] != min_pixel_value:
                    pixel_array.append(y)        
        for z in range(len(pixel_array)-1):
            scalar_difference = pixel_array[z+1] - pixel_array[z]
            if not scalar_difference in image_scale_y:
                image_scale_y.append(int(scalar_difference))                
          
    # image_scale_array = image_scale_array.sort()  
    image_scale_y.sort(key=sortFunc)    
    for count in range(len(image_scale_y)):
        if image_scale_y[count] < int(1.5 *image_scale_y[0]):
            if not image_scale_y[count] in image_scale_array:
                image_scale_array.append(image_scale_y[count])

    x = 0
    while x < len(image_scale_array):
        # print(image_scale_array[x], image_scale_array[x]+1)
        if image_scale_array[x] == (image_scale_array[x-1]+1):
            image_scale_array.pop(x)
        x += 1
            
    return image_scale_array

def sortFunc(e):
    return int(e)
    