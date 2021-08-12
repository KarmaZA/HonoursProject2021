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
    source_image_gray = None
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


def CalcScale(PointSet):
    scale_to_return = [0,0]
    
    # Sum the points together on a y scale and a x scale
    # calc distance on each scale
    sum_x_array = []
    sum_y_array = []
    #Find min x and y
    min_x = 100
    min_y = 100
    for point in PointSet:
        if(min_x > point.x):
            min_x = int(point.x)
        if(min_y > point.y):
            min_y = int(point.y)
    for point in PointSet:
        if (point.x == min_x):
            sum_x_array.append(int(point.x+point.y))
        if (point.y == min_y):
            sum_y_array.append(int(point.x+point.y))
         
    #TODO
    #REWRITE this into the average difference of the arrays
    min_x = (sum_x_array[1] - sum_x_array[0]) * 10
    min_y = (sum_y_array[1] - sum_y_array[0]) * 10
    print(sum_x_array, sum_y_array)
    print('The Square Pattern side length is ' + str(int((min_x+min_y)/2)))
    print('The Rectangle Pattern side length is: ' + str(min_y) + ' and ' + str(min_x))
    print('The length used for the triangle template is: ' + str(min(min_x,min_y)))
    scale_to_return = [min_x, min_y]
    return scale_to_return
    