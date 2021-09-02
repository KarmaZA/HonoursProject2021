# This class will take input of the pointset and calculate the rotation of the image
from LinkedList import LinkedList, Node
from re import A
from sklearn.neighbors import KDTree
from shapely.geometry.point import Point
from shapely.geometry.multipoint import MultiPoint

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import math

from haversine import Unit
import haversine as hs
import random


def normaliseData(PointSet):
    
    dataset = KDTree(PointSet)
    nearest_dist, nearest_ind = dataset.query(PointSet, k=4)
    
    #INPUT here for number sampling
    sample_Points = random.sample(range(0, len(PointSet)), 10)
    
    for x in range(1):#len(sample_Points)):
        i = sample_Points[x]
        # List of angles between points
        angle_list = []
        # List of points from nearest_ind
        point_list = []
        # Points that make up the row
        row_list = []
        linked_list_test = LinkedList()
        
        # Setting up the base case
        # Origin point
        point_list.append(nearest_ind[i,0])
        row_list.append(Point(PointSet[point_list[-1]].x, PointSet[point_list[-1]].y)) 
        point_index = nearest_ind[i,1]
        # Origin angle
        angle = calcLineRotation(PointSet[nearest_ind[i,0]], PointSet[point_index])  
         
        building_line = True

        print("Origin point index: " + str(point_list[0]) + " with an angle of " + str(angle))
        
        while building_line == True:
            #Add data to lists
            angle_list.append(angle)
            point_list.append(point_index)  
            row_list.append(Point(PointSet[point_list[-1]].x, PointSet[point_list[-1]].y))        

            # Run the check from furtherest to closest
            # Results in closest corresponding angle
            angle_average = AverageAngle(angle_list)
            for y in range(4):
                value_check = int(nearest_ind[point_index][y])
                # Point hasn't been dealt with before
                if not(value_check in point_list):
                    point_index = nearest_ind[point_index][y]
                    # print(value_check, point_list)
                    # print(count, len(angle_list)-1)
                    angle_check = calcLineRotation(row_list[-1], PointSet[value_check])
                    if (AnglesInRange(angle_list[-1], angle_check,15)) or (AnglesInRange(angle_average, angle_check,15)):
                        point_index = nearest_ind[point_index][y]
                        linked_list_test.add_to_head(Node(nearest_ind[point_index][y]))
                        if AnglesInRange(angle_average, angle_check,15):
                            print("average")
                        else: 
                            print("current")
                        # print(nearest_ind[point_index][y])
               
            if point_index in point_list:
                building_line = False

            
            #########################
            # Also need to build the row going in the opposite directions
            # ReImplement it with a Linked List
            # Add average angle to determine best route
            #########################
            
            # angle = calcLineRotation(row_list[count-1], Point(PointSet[point_list[count]].x, PointSet[point_list[count]].y))
            # print(angle)
            # angle = calcLineRotation(row_list[count-1], Point(PointSet[0].x, PointSet[0].y))
            # print(angle)
            # building_line = AnglesInRange(angle_list[count],angle)
            # print(angle_list[count],angle)
        # print(point_list)
        # print("Linked List")
        # print(linked_list_test)
        xs = [point.x for point in PointSet]
        ys = [point.y for point in PointSet]
        plt.scatter(xs,ys, color = 'black')
        x1s = [point.x for point in row_list]
        y1s = [point.y for point in row_list]
        colors = cm.rainbow(np.linspace(0, 1, len(y1s)))
        for x, y, c in zip(x1s, y1s, colors):
            plt.scatter(x, y, color=c)
        # plt.scatter(x1s,y1s, color = 'black')
        plt.show()
        return AverageAngle(angle_list)
        
        
def AverageAngle(angle_list):
    count = 0
    for angle in angle_list:
        count+= angle
    return (count/len(angle_list))
        

def calcLineRotation(origin_point, endpoint):
    x1, x2, y1, y2 = (origin_point.x, endpoint.x, origin_point.y, endpoint.y)
    angle_theta = math.atan2(y2-y1, x2-x1)
    return math.degrees(angle_theta)           
        
        
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
    
    # https://stackoverflow.com/questions/48126771/nearest-neighbour-search-kdtree/48127117#48127117
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


#Where point1 and2 are from PointSet. Returns distance in meters
def calcScaleUnitValues(point1,point2):
    loc1 = (point1.x, point1.y)
    loc2 = (point2.x, point2.y)
    return hs.haversine(loc1, loc2, unit=Unit.METERS)
    
