# This class will take input of the pointset and calculate the rotation of the image
import SimilarityMeasures as SM

import cv2
import imutils

def calcImageRotation(Pointset):
    rotation = 0 # Degrees
    image = cv2.imread('Images/TemplateLine.png', 0)
    main_image = cv2.imread('Images/MainImage.png', 0)
    rotation_correlation_list = []
    # Only need to rotate 180 degrees
    for x in range(8):
        rotated = imutils.rotate(image,angle=(x*45))
        correlation_measure = SM.templateMatching_correlation_score(main_image, image)
        rotation_correlation_list.append(correlation_measure)
        #window_show_sized = cv2.resize(rotated, (960, 540));
        #cv2.imshow("Matched image", window_show_sized)
        #cv2.waitKey()
        #cv2.destroyAllWindows()
        
    print("The correlation list is")
    print(rotation_correlation_list)
    
    #Calc Scale will return an array of mean distances. These could number from 1 to several
    # Like will have to recode the entire section
def CalcScale(PointSet):
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
    print()
    #print(sum_x_array, sum_y_array)
    print('The Square Pattern side length is ' + str(int((min_x+min_y)/2)))
    square_length = int((min_x+min_y)/2)

    if min_y != min_x:
        print('The Rectangle Pattern side length is: ' + str(min_y) + ' and ' + str(min_x))
    else:
        min_y += int(0.5*min_x)
        min_x = int(min_x*0.5)
        print("Width and height are equal. Likely output is a square pattern. Changing rectangle dimensions to avoid complications.")
        ################################## Maybe find a way to not use the template instead
    rectangle_height = min_y
    rectangle_width = min_x
    
    print('The length used for the triangle template is: ' + str(min(min_x,min_y)))
    triangle_length = min(min_x,min_y)  