# This class will take input of the pointset and calculate the rotation of the image
from re import split
from LinkedList import LinkedList, Node
from sklearn.neighbors import KDTree

from pyproj import Proj, Transformer

from shapely.geometry import Point, MultiPoint, LineString
import shapely.ops as sp_ops

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from math import radians, cos, sin, atan2, degrees
import random


def convertPointsToInt(PointSet):
    set_to_return= []
    x_min, y_min, x_max, y_max = (400,400,-400,-400)
    # x_min, y_min, x_max, y_max = (0,0, -0.0058, 0.006778)
    for point in PointSet:
        if point.x < x_min : x_min = point.x
        if point.y < y_min : y_min = point.y
        if point.x > x_max : x_max = point.x
        if point.y > y_max : y_max = point.y
    x_max = x_min + (-0.0058)
    # x_min -= x_min
    y_min = y_max - 0.00006778
    # y_min -= y_min
    print(x_min, y_min, x_max, y_max)
    for point in PointSet:
        if point.y > y_min: 
            set_to_return.append(Point(point.x, point.y))
            print("here")
        else: 
            print(point.y)
        # if ((point.x > x_min) and (point.x < x_max)) and ((point.y > y_min) and (point.y < y_max)):
        #     set_to_return.append(Point(point.x, point.y))
        #     print("here")
            
    # delta_y = (y_max-y_min)/100        
    print("A visual depictions of your orchard")
    xs = [point.x for point in set_to_return]
    ys = [point.y for point in set_to_return]
    plt.scatter(xs,ys, color = 'black')
    # plt.yticks(np.arange(y_min, y_max, delta_y))
    plt.savefig('OrchardGraph.png')
    plt.show()
    x1s = [point.x for point in PointSet]
    y1s = [point.y for point in PointSet]
    plt.scatter(x1s,y1s, color = 'black')
    plt.scatter(xs,ys, color = 'blue')
    plt.show()
    return MultiPoint(PointSet)
    
    # set_to_return.append(Point(0,0))
    # delta_x, delta_y = (-PointSet[0].x, -PointSet[0].y)
    # float_count = 10 **(len(str(PointSet[0].x).split('.')[1]))
    
    # for k in range(1, len(PointSet)):
    #     # Point1 = Point(PointSet[k-1].x, PointSet[k-1].y)
    #     # Point2 = 
    #     # line_distance = LineString([PointSet[k-1], PointSet[k]])
    #     # # line_distance.srid = 4326
    #     # my_transformer = Transformer.from_crs('EPSG:4326', 'EPSG:3857', always_xy=True)
    #     # distnace = sp_ops.transform(my_transformer.transform, line_distance)
    #     # print(distnace.length)
    #     # angle = calcLineRotation(PointSet[k-1], PointSet[k])
    #     # delta_x = PointSet[k-1].x * cos(angle)
    #     # delta_y = PointSet[k-1].y * sin(angle)
    #     # delta_x *= int(distnace.length)
    #     # delta_y *= int(distnace.length)
        
    #     # set_to_return.append(Point((set_to_return[k-1].x + delta_x), (set_to_return[k-1].y + delta_y)))
    #     set_to_return.append(Point((PointSet[k].x + delta_x), (PointSet[k].y + delta_y)))
        
    #     set_to_return[k] = Point(int(set_to_return[k].x*float_count),int(set_to_return[k].y*float_count))
    # print("xy delta")
    # print(delta_x/len(PointSet))
    # print(delta_y/len(PointSet))    
    # xs = [point.x for point in set_to_return]
    # ys = [point.y for point in set_to_return]
    # plt.scatter(xs,ys, color = 'black')
    # plt.show()
    # return MultiPoint(set_to_return)


# #Where point1 and2 are from PointSet. Returns distance in meters
# def calcScaleUnitValues(point1,point2):
#     loc1 = (point1.x, point1.y)
#     loc2 = (point2.x, point2.y)
#     return hs.haversine(loc1, loc2, unit=Unit.METERS)

def normaliseData(PointSet):
    dataset = KDTree(PointSet)
    nearest_dist, nearest_ind = dataset.query(PointSet, k=4)
    
    #INPUT here for number sampling
    sample_Points = random.sample(range(0, len(PointSet)), 10)
    
    z = 745
    point_list = []
    for i in range(10):
        
        row_list = []
        
        for y in range(4):
            row_list.append(Point(PointSet[nearest_ind[z][y]].x, PointSet[nearest_ind[z][y]].y))    
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
        point_list.append(z)
        count = 1
        while z in point_list:
            if nearest_ind[z][count] not in point_list:
                z = nearest_ind[z][count]
            count += 1
            if count > 4:
                print("done")
                exit()
        print(nearest_ind[z], point_list)
    
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
        angle_list.append(angle)
        building_line = True

        print("Origin point index: " + str(point_list[0]) + " with an angle of " + str(angle))
        
        point_list.append(nearest_ind[i,1])
        row_list.append(Point(PointSet[point_list[-1]].x, PointSet[point_list[-1]].y)) 
        point_index = nearest_ind[i,2]
        # Origin angle
        angle = calcLineRotation(PointSet[nearest_ind[i,0]], PointSet[point_index]) 
        if (angle - angle_list[0]) > ((angle*-1) -angle_list[0]):
            print(angle)
            angle *= -1 
         
        print(angle_list)
        building_line = True

        print("Origin point index: " + str(point_list[0]) + " with an angle of " + str(angle))
        
        while building_line == True:
            #Add data to lists
            angle_list.append(angle)
            print(AverageAngle(angle_list))
            point_list.append(point_index)  
            row_list.append(Point(PointSet[point_list[-1]].x, PointSet[point_list[-1]].y))        

            # Run the check from furtherest to closest
            # Results in closest corresponding angle
            angle_average = AverageAngle(angle_list)
            for y in range(4):
                value_check = nearest_ind[point_index][y]
                
                
                
                # Point hasn't been dealt with before
                if not(value_check in point_list):
                    point_index = nearest_ind[point_index][y]
                    # print(value_check, point_list)
                    # print(count, len(angle_list)-1)
                    angle_check = calcLineRotation(row_list[-1], PointSet[value_check])
                    angle_check_origin = calcLineRotation(row_list[0], PointSet[value_check])
                    if (AnglesInRange(angle_list[-1], angle_check,15)) or (AnglesInRange(angle_average, angle_check,15)):
                        point_index = nearest_ind[point_index][y]
                        # linked_list_test.add_to_head(Node(nearest_ind[point_index][y]))
                        if AnglesInRange(angle_average, angle_check,15):
                            print("average")
                        else: 
                            print("current")
                        # print(nearest_ind[point_index][y])
                    elif (AnglesInRange(angle_list[-1], angle_check_origin,15)) or (AnglesInRange(angle_average, angle_check_origin,15)):
                        point_index = nearest_ind[point_index][y]
               
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


    
