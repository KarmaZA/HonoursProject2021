# This class will take input of the pointset and calculate the rotation of the image
import SimilarityMeasures as SM

import cv2
import imutils
from scipy.spatial import distance
from sklearn.neighbors import KDTree
import numpy as np
import math

def calcLineRotation(x1, x2, y1, y2):
    angle_theta = math.atan2(y2-y1, x2-x1)
    return math.degrees(angle_theta)
    

def calcImageRotation(PointSet):
    rotation_to_return = []
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
                if not np.round(angle,2) in rotation_to_return:
                    rotation_to_return.append(np.round(angle,2)) #ROUND DISTANCE TO 2 FLOATING POINTS
                    
    # print(rotation_to_return)
    return rotation_to_return
    
    #Calc Scale will return an array of mean distances. These could number from 1 to several
def CalcScale(PointSet):
    distance_to_return = []  
    
    # https://stackoverflow.com/questions/48126771/nearest-neighbour-search-kdtree/48127117#48127117
    dataset = KDTree(PointSet)
    nearest_dist, nearest_ind = dataset.query(PointSet, k=4)
    # print(dataset)
    # print(nearest_dist[:, 1:5])
    # print(nearest_ind[:, 1])
    
    # Change to random point checking than O(n2)
    for x in range(len(PointSet)):
        for y in range(3):
            if not np.round(nearest_dist[x,y+1],1) in distance_to_return:
                distance_to_return.append(np.round(nearest_dist[x,y+1],1)) #ROUND DISTANCE TO 2 FLOATING POINTS
                print(nearest_dist[x,y+1])                          # ^ CHECK ROUNDING
            
    return distance_to_return


