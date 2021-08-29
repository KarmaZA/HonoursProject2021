# This class will take input of the pointset and calculate the rotation of the image
from sklearn.neighbors import KDTree
import numpy as np
import math

def calcLineRotation(x1, x2, y1, y2):
    angle_theta = math.atan2(y2-y1, x2-x1)
    return math.degrees(angle_theta)
    

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
                
    threshold = int(len(PointSet)*0.3) #MAGIC NUMBER CHECK AND TEST
    distance_To_Return = []
    for values in distance_values:
        if values[1] > threshold and (values[0] != 0.0):
            distance_To_Return.append(values[0])
    print('Detected Scale Variations')
    print(distance_To_Return)
    return distance_To_Return


def calcScaleUnitValues(PointSet):
        # returns the scale unit
    # i.e. scale number * unit = irl scale
    decimal_count = int(len(str(PointSet[0].x).split('.')[1]))
    return decimal_count
    
