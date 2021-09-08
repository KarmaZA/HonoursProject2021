# This class will take input of the pointset and calculate the rotation of the image
from re import split

from matplotlib.collections import QuadMesh
from LinkedList import LinkedList, Node
from sklearn.neighbors import KDTree

from shapely.geometry import Point, MultiPoint

import matplotlib.pyplot as plt
import numpy as np
from math import atan2, degrees
import random


def GenerateSubImages(PointSet):
    count = 0
    x_min, y_min, x_max, y_max = (400,400,-400,-400)
    for point in PointSet:
        if point.x < x_min : x_min = point.x
        if point.y < y_min : y_min = point.y
        if point.x > x_max : x_max = point.x
        if point.y > y_max : y_max = point.y
        
    max_image_number = int((len(PointSet)/400)+1)
    delta_x = (x_max-x_min)/max_image_number
    delta_y = (y_max-y_min)/max_image_number

    for x in range (max_image_number):    
        y_max = y_min + delta_y 
        for y in range(max_image_number):                                   
            set_to_return= []    
            # Set boundaries for edges of sub image
            x_max = x_min + delta_x             
            print(x_min, y_min, x_max, y_max)
            for point in PointSet:
                if ((point.x > x_min) and (point.x < x_max)) and ((point.y > y_min) and (point.y < y_max)):
                    set_to_return.append(Point(point.x, point.y))
            print(len(set_to_return))
            if (len(set_to_return) > 25):
                    
                xs = [point.x for point in set_to_return]
                ys = [point.y for point in set_to_return]
                plt.gca().set_aspect('equal')
                plt.scatter(xs,ys, color = 'blue')
                # plt.figure(frameon=False)
                plt.axis('off')
                plt.savefig('Images/MainImage' + str(count) + '.png')
                plt.clf()
                count +=1 
            
            #Update the boundaries of the sub - image
            x_min = x_max            
            
        y_min = y_max
        x_min -= (delta_x*max_image_number)
    return count


def normaliseData(PointSet):
       
    dataset = KDTree(PointSet)
    nearest_dist, nearest_ind = dataset.query(PointSet, k=4)
    scale_intra = 0
    
    #Calculate the average intra_row scale
    for point in nearest_dist:
        scale_intra += point[1]
    scale_intra /= len(nearest_dist)
    print("Average scale: " + str(scale_intra))
    
    sampled_points = []
    weighted_average_angles = []
    for i in range(10):
        angle_list = []
        point_list = []
        # If for values not in point line angle is not in range make false
        building_line = True
        # for i in range(1):#0):
        z = random.randint(0, len(PointSet))
        while z in sampled_points:
            z = random.randint(0, len(PointSet))
            print(z)
        row_list = []
        # Origin Point
        point_list.append(nearest_ind[z][0])
        point_list.append(nearest_ind[z][1])
        angle_list.append(calcLineRotation(PointSet[point_list[0]], PointSet[point_list[1]]))
        print("Origin point at " + str(point_list[0]))
        
        for i in range(2,4):
            angle = calcLineRotation(PointSet[point_list[0]], PointSet[nearest_ind[z][i]])
            if AnglesInRange(angle_list[0], angle, 30):
                point_list.append(nearest_ind[z][i])
                angle_list.append(angle)
                
        print("data")
        print(point_list)
        print(angle_list)
            
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
            print(point_list)
            
        angle_list_inverse = []
        print("##########################################################")
        building_line = True
        while building_line:
            print("Inverse test")
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
                    print(angle_origin, average_angle)
                    #Condition below super important for detections
                    if (AnglesInRange(angle_origin, average_angle, 10)):# and (AnglesInRange(angle_list[-1], angle_instant, 30)):
                        point_list.insert(nearest_ind[z][count],0)
                        angle_list_inverse.append(angle_instant)
                        building_line = True
                    if (AnglesInRange(angle_origin, average_angle, 10)):
                            print("origin success") 
                count += 1
                
        print("end of list")
        print(point_list)
              
        print(nearest_ind[point_list[-1]])
        for point in point_list:
            sampled_points.append(point)
        weighted_average_angles.append(AverageAngle(angle_list))#, len(point_list)])

        
        
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
    # colors = cm.rainbow(np.linspace(0, 1, len(y1s)))
    # for x, y, c in zip(x1s, y1s, colors):
    #     plt.scatter(x, y, color=c)
    plt.scatter(x1s,y1s, color = 'red')
    x2s = [point.x for point in row_list2]
    y2s = [point.y for point in row_list2]
    plt.scatter(x2s,y2s, color = 'blue')
    plt.show()
    point_list.append(z)
    return (PointSet, scale_intra, weighted_average_angles)

def calcWeightedAverageAngle(angle_list):
    count = 0
    angle_avg = 0
    countneg = 0
    angle_avgneg = 0
    for angle in angle_list:
        if angle > 0:
            angle_avg += angle
            count += 1
        else:
            angle_avgneg += angle
            countneg += 1
            
    if count >= countneg:
        return angle_avg/count
    else:
        return angle_avgneg/countneg        
        
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
    # print(abs(Angle1-Angle2))
    if abs(Angle1-Angle2) <= threshold:
        return True
    else:
        return False
    

def calcImageRotation(PointSet):
    rotation_values = []
    dataset = KDTree(PointSet)
    nearest_dist, nearest_ind = dataset.query(PointSet, k=4)
    for x in range(len(PointSet)):
        origin_point_x = PointSet[nearest_ind[x,0]].x
        origin_point_y = PointSet[nearest_ind[x,0]].y
        # print(origin_point_x, origin_point_y)
        for y in range(3):
            # angle =  nearest_dist[x,y+1]
            endpoint_x = PointSet[nearest_ind[x,y+1]].x
            endpoint_y = PointSet[nearest_ind[x,y+1]].y
            if(not(nearest_ind[x,0] == 0) and not(nearest_ind[x,y+1] == 0)):
                angle = calcLineRotation(origin_point_x, endpoint_x, origin_point_y, endpoint_y)
                in_List = True
                for values in rotation_values:
                    # print(values[1])
                    if np.round(angle,1) == values[0]:
                        values[1] += 1
                        in_List = False
                if in_List:
                    rotation_values.append([np.round(angle,1),0])                  
            
    print("Detected Rotations")
    threshold = int(len(PointSet) * 0.3)
    rotation_To_Return = []
    for values in rotation_values:
        if values[1] > threshold:
            rotation_To_Return.append(values[0])
      
    print(rotation_To_Return)
    print()
    return rotation_To_Return
    
    #Calc Scale will return an array of mean distances. These could number from 1 to several
def CalcScale(PointSet):
    distance_values = []  
    dataset = KDTree(PointSet)
    nearest_dist, nearest_ind = dataset.query(PointSet, k=4)
    
    # Change to random point checking than O(n2)
    for x in range(len(PointSet)):
        for y in range(3):
            ######
            # Check if in array
            in_List = True
            for values in distance_values:
                # print(values[1])
                if np.round(nearest_dist[x,y+1],1) == values[0]:
                    values[1] += 1
                    in_List = False
            if in_List:
                 distance_values.append([np.round(nearest_dist[x,y+1],1),0])
                
    threshold = int(len(PointSet)*0.1) #MAGIC NUMBER CHECK AND TEST
    distance_To_Return = []
    while distance_To_Return == []:
        for values in distance_values:
            print(values)
            if values[1] > threshold and (values[0] != 0.0):
                distance_To_Return.append(values[0])
            threshold -= int(len(PointSet)*0.5)
    print('Detected Scale Variations')
    print(distance_To_Return)
    return distance_To_Return


    
