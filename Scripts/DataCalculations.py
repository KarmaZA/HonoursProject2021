# A file that does the calculations to solve the issue of rotation and scale for Template Matching23

from LinkedList import LinkedList, Node
from sklearn.neighbors import KDTree
from shapely.geometry import Point
from math import atan2, degrees

import matplotlib.pyplot as plt
import random

"""Breaks up the pointset into a number of sub images that can be efficiently dealt with in the Template Matching step"""
def GenerateSubImages(PointSet):
    count = 0
    x_min, y_min, x_max, y_max = (400,400,-400,-400)
    for point in PointSet:
        if point.x < x_min : x_min = point.x
        if point.y < y_min : y_min = point.y
        if point.x > x_max : x_max = point.x
        if point.y > y_max : y_max = point.y

    length_test = len(PointSet)
    if length_test < 1500:
        max_image_number = 3
    elif length_test < 2550:
        max_image_number = 4
    elif length_test < 3550:
        max_image_number = 5
    elif length_test < 4550:
        max_image_number = 6
    elif length_test < 5550:
        max_image_number = 7
    else:
        max_image_number = 7 + int((len(PointSet - length_test))/1000)

    delta_x = (x_max-x_min)/max_image_number
    delta_y = (y_max-y_min)/max_image_number
    # print(delta_x,delta_y)
    test_set = []


    for x in range (max_image_number):    
        y_max = y_min + delta_y 
        for y in range(max_image_number):                                   
            set_to_return= []    
            # Set boundaries for edges of sub image
            x_max = x_min + delta_x             
            for point in PointSet:
                if ((point.x >= x_min) and (point.x <= x_max)) and ((point.y >= y_min) and (point.y <= y_max)):
                    set_to_return.append(Point(point.x, point.y))
            if (len(set_to_return) > 99):          
                xs = [point.x for point in set_to_return]
                ys = [point.y for point in set_to_return]
                plt.gca().set_aspect('equal')
                plt.scatter(xs,ys, color = 'black')
                plt.axis('off') # So the image only has points
                plt.savefig('Images/MainImage' + str(count) + '.png')
                plt.clf()
                count +=1 
            #Update the boundaries of the sub - image
            x_min = x_max                     
        y_min = y_max
        x_min -= (delta_x*max_image_number)
    return count

"""Row detection method that displays the detected rows
and the returns max trees per row and a list of the detected angles"""
def rowDetection(PointSet, dataset):
    max_Tree_per_Row = 0
    nearest_dist, nearest_ind = dataset.query(PointSet, k=4)
    
    sampled_points = []
    row_count = 0
    weighted_average_angles = []
    while row_count < 10:
        angle_list = []
        point_list = []
        # If for values not in point line angle is not in range make false
        building_line = True
        z = random.randint(0, len(PointSet)-1)
        while z in sampled_points:
            z = random.randint(0, len(PointSet)-1)
            # print(z)
        row_list = []
        # Origin Point
        point_list.append(nearest_ind[z][0])
        point_list.append(nearest_ind[z][1])
        angle_list.append(calcLineRotation(PointSet[point_list[0]], PointSet[point_list[1]]))
        
        for i in range(2,4):
            angle = calcLineRotation(PointSet[point_list[0]], PointSet[nearest_ind[z][i]])
            if AnglesInRange(angle_list[0], angle, 30):
                point_list.append(nearest_ind[z][i])
                angle_list.append(angle)

        while building_line:
            z = point_list[-1]
            building_line = False
            average_angle = AverageAngle(angle_list)
            
            count = 1
            while(building_line == False) and (count < 4):
                if not (nearest_ind[z][count] in point_list):
                    angle_origin = calcLineRotation(PointSet[point_list[0]], PointSet[nearest_ind[z][count]])
                    angle_instant = calcLineRotation(PointSet[point_list[-1]], PointSet[nearest_ind[z][count]])
                    #Condition below super important for detections
                    if (AnglesInRange(angle_origin, average_angle, 10)) and (AnglesInRange(angle_list[-1], angle_instant, 30)):
                        point_list.append(nearest_ind[z][count])
                        angle_list.append(angle_instant)
                        building_line = True
                count += 1
            # print(point_list)
            
        angle_list_inverse = []
        # print("##########################################################")
        building_line = True
        while building_line:
            # print("Inverse test")
            z = point_list[0]
            building_line = False
            average_angle = AverageAngle(angle_list)
            if average_angle > 0:
                average_angle -= 180
            else:
                average_angle += 180
            
            count = 1
            while(building_line == False) and (count < 4):               
                if not (nearest_ind[z][count] in point_list):
                    angle_origin = calcLineRotation(PointSet[point_list[-1]], PointSet[nearest_ind[z][count]])
                    angle_instant = calcLineRotation(PointSet[point_list[0]], PointSet[nearest_ind[z][count]])
                    # if (nearest_ind[z][count] in point_list):
                    #     print("FAIL")
                    #Condition below super important for detections
                    if (AnglesInRange(angle_origin, average_angle, 10)) and (AnglesInRange(angle_list[-1], angle_instant, 30)):
                        point_list.insert(0,nearest_ind[z][count])
                        angle_list_inverse.append(angle_instant)
                        building_line = True
                count += 1          
        for point in point_list:
            sampled_points.append(point)
        if len(point_list) > 10:
            weighted_average_angles.append(AverageAngle(angle_list))#, len(point_list)])
            row_count += 1
        if len(point_list) > max_Tree_per_Row:
            max_Tree_per_Row = len(point_list)
        
    for coords in sampled_points:
        row_list.append(Point(PointSet[coords].x, PointSet[coords].y))  
    row_list2 = [] 
    for coords in nearest_ind[point_list[-1]]:
        row_list2.append(Point(PointSet[coords].x, PointSet[coords].y))   
    
    xs = [point.x for point in PointSet]
    ys = [point.y for point in PointSet]
    plt.scatter(xs,ys, color = 'black')
    x1s = [point.x for point in row_list]
    y1s = [point.y for point in row_list]
    plt.scatter(x1s,y1s, color = 'red')
    # x2s = [point.x for point in row_list2]
    # y2s = [point.y for point in row_list2]
    # plt.scatter(x2s,y2s, color = 'blue')
    plt.title("Row Detection")
    plt.show()
    point_list.append(z)
    # print(weighted_average_angles)
    return (PointSet, weighted_average_angles, max_Tree_per_Row)

"""Calculates the most common angle range in a list
or if no most common returns the average of the list"""
def calcWeightedAverageAngle(angle_list):
    count = 0
    angle_avg = 0
    countneg = 0
    angle_avgneg = 0
    for angle in angle_list:
        if angle > 0:
            angle_avg += angle
            count += 1
        elif angle < 0:
            angle_avgneg += angle
            countneg += 1

    if angle_list.count(0) > 3:
        return 0      
    elif count >= countneg:
        return angle_avg/count
    else:
        return angle_avgneg/countneg

"""Calculates the most common angle range in a list
or if no most common returns the average of the list"""
def getCommonAngle(angle_list):
    angle_list.sort()
    curr_angle = 0
    max_count = 0
    count = 0
    sum_Arr = []
    final_Arr = []
    for x in range(len(angle_list)-1):
        sum_Arr.append(angle_list[x])
        if AnglesInRange(angle_list[x], angle_list[x+1], 10):
            count += 1
        else:
            if count > max_count:
                final_Arr = sum_Arr
                max_count = count
                count = 0
            sum_Arr = []
    # print(final_Arr, max_count)
    for angle in final_Arr:
        curr_angle += angle
    max_count = len(final_Arr)
    if max_count > 2:
        # print('here')
        return int(curr_angle/len(final_Arr))     
    else:
        #Result is arbitrary take an average
        return calcWeightedAverageAngle(angle_list)
        
def AverageAngle(angle_list):
    count = 0
    for angle in angle_list:
        count+= angle
    return (count/len(angle_list))
        

def calcLineRotation(origin_point, endpoint):
    x1, x2, y1, y2 = (origin_point.x, endpoint.x, origin_point.y, endpoint.y)
    angle_theta = atan2(y2-y1, x2-x1)
    return degrees(angle_theta)           
        
        
def AnglesInRange(Angle1, Angle2, threshold):
    if abs(Angle1-Angle2) <= threshold:
        return True
    else:
        return False

def RWPointDistance(p1, p2):
    return p2-p1
