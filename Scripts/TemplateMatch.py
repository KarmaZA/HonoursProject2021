# Developed By Jonathon Everatt
# This file will contain template matching similarity measures for the template matching algorithms

import cv2
import numpy as np
from shapely.geometry import Point, MultiPoint
import imageio

"""Implementation of OpenCV template matching method. Input is the source image and desired template.
Returns a list of matches in 0.1 correlation decrements starting from 1"""
def templateMatching_correlation(source_image, template_image):
    threshold = 0.9
    source_image_gray = source_image
    res = cv2.matchTemplate(source_image_gray, template_image, cv2.TM_CCOEFF_NORMED)
    correlation_array = []
    # 0 (1-0.9), 1 (0.9-0.8), 2 (0.8-0.7), 3 (0.7-0.6), 4 (0.6-0.5), 5 (0.5-0.4), 6 (0.4-0.3)   
    count = 0
    
    for x in range(7):       
        curr_count = 0   
        loc = np.where( res >= threshold)
        width, height = template_image.shape
        for pt in zip(*loc[::-1]):
            curr_count += 1

        correlation_array.append(curr_count)
        count += curr_count
        threshold -= 0.1
    return correlation_array

"""Used to display the match points of the template. adjust line 42. Only used in experiments"""
def templateMatching_display(source_image, template_image):
    threshold = 0.5
    source_image_gray = source_image
    res = cv2.matchTemplate(source_image_gray, template_image, cv2.TM_CCOEFF_NORMED)
    loc = np.where( res >= threshold)
    width, height = template_image.shape
    count = 0
    for pt in zip(*loc[::-1]):
        cv2.rectangle(source_image_gray, pt, (pt[0] + width, pt[1] + height), (128,128,128), 2)
        count += 1
        if count > 1400:
            cv2.imshow("Displayed Match", source_image_gray)
            cv2.waitKey(0)

"""Make all non-black pixels white. if value not 0 then 255"""
def cleanTheGraph(source_image):
    width, height = source_image.shape
    for x in range(width):
        for y in range(height):
            if source_image[x][y] > 0:
                source_image[x][y] = 255
    return source_image

"""calculates the scale parameters for the template matching method.
Assumes the rows are aligned to one of the axes.
returns most commonly detected scales"""
def CalcScale(image):
    dict = {}
    min_pixel_value = 0
    width, height  = image.shape    
    image_scale_x = []    
    image_scale_y = []
    
    ## Vertical Search
    for x in range(width):
        pixel_array = []
        for y in range(height-1):
            if image[x][y] == min_pixel_value:
                # We are on a black pixel
                if image[x][y+1] != min_pixel_value:
                    pixel_array.append(y)        
        for z in range(len(pixel_array)-1):
            scalar_difference = pixel_array[z+1] - pixel_array[z]
            if scalar_difference in dict.keys():
                dict[scalar_difference] += 1
            else:
                dict[scalar_difference] = 1
    max_count = 0
    for key in dict.keys():     
        if dict[key] > max_count:
            max_count = dict[key]
    for key in dict.keys():
        if key > 10 and int(dict[key]) > (0.75*max_count):
            image_scale_y.append(key)
    image_scale_y.sort(key=sortFunc)  
   
                
################### Horizontal search 
    dict = {}
    image_scale_x = []
    for y in range(height-1):
        pixel_array = []
        for x in range(width):
            if image[x][y] == min_pixel_value:
                if image[x][y+1] != min_pixel_value:
                    pixel_array.append(x) 
                          
        for z in range(len(pixel_array)-1):
            scalar_difference = pixel_array[z+1] - pixel_array[z]
            if scalar_difference in dict.keys():
                dict[scalar_difference] += 1
            else:
                dict[scalar_difference] = 1
 
    max_count = 0
    for key in dict.keys():     
        if dict[key] > max_count and key > 10:
            max_count = dict[key]
    for key in dict.keys():
        if key > 10 and int(dict[key]) > (0.75*max_count):
                image_scale_x.append(key)

    image_scale_x.sort(key=sortFunc) 
    
    return image_scale_y, image_scale_x


def sortFunc(e):
    return int(e)

    