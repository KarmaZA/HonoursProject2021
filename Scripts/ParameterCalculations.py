# A file for calculating the parameters to be extracted from the data

from LinkedList import LinkedList, Node
from sklearn.neighbors import KDTree
from shapely.geometry import Point

import matplotlib.pyplot as plt
import DataCalculations

def CornerTreeCoords(PointSet):
    min_x, min_y, max_x, max_y = (400,400,-400,-400)
    for point in PointSet:
        if point.x < min_x:
            point_min_x = point
            min_x = point.x
        elif point.y < min_y:
            point_min_y = point
            min_y = point.y
        elif point.x > max_x:
            point_max_x = point
            max_x = point.x
        elif point.y > max_y:
            point_max_y = point
            max_y = point.y
    
    set_to_return = []
    set_to_return.append(Point(point_min_x.x, point_min_x.y))
    set_to_return.append(Point(point_min_y.x, point_min_y.y))
    set_to_return.append(Point(point_max_x.x, point_max_x.y))
    set_to_return.append(Point(point_max_y.x, point_max_y.y))

    return set_to_return

def countRowNumbers(PointSet, angle, dataset):
    row_count = 0
    inter_spacing = 0
    spacing_list = []
    point_list = []
    angle_perp_1 = (angle + 90) % 180
    angle_perp_2 = (angle - 90) % 180
    nearest_dist, nearest_ind = dataset.query(PointSet, k=8)

    spacing_list.append(random.randint(0, len(PointSet)))
    row_count += 1

    count_rows = True
    
    while count_rows:
        count_rows = False
        for x in range(8):
            angle_check = calcLineRotation(PointSet[nearest_ind[point_list[-1]][0]],PointSet[nearest_ind[point_list[-1]][x]])
            if DataCalculations.AnglesInRange(angle_perp_1, angle_check, 23):
                row_count += 1
                point_list.append(nearest_ind[point_list[-1]][x])
                spacing_list.append(nearest_dist[point_list[-1]][x])
                count_rows = True
                break

    # Count rows in opposite direction
    while count_rows:
        count_rows = False
        for x in range(8):
            angle_check = calcLineRotation(PointSet[nearest_ind[point_list[0]][0]],PointSet[nearest_ind[point_list[0]][x]])
            if DataCalculations.AnglesInRange(angle_perp_1, angle_check, 23):
                row_count += 1
                point_list.insert(0, nearest_ind[point_list[0]][x])
                spacing_list.append(nearest_dist[point_list[0]][x])
                count_rows = True
                break

    for spac in spacing_list:
        inter_spacing += spac

    inter_spacing /= len(spacing_list)

    #If spacing is an outlier it's probably a road or ditch
    road_Thresh = int(2*inter_spacing)
    road_count = 0
    for spac in spacing_list:
        if spac > road_Thresh:
            road_count +=1 
    
    return (row_count, inter_spacing, road_count)


def meanRowCount(PointSet):
    meanCount = 0
    #THIS SHOULD PROBABLY BE DONE DURING DETECTION
    return meanCount

def calcScaleIntra(dataset):
    nearest_dist, nearest_ind = dataset.query(PointSet, k=4)
    scale_intra = 0   
    #Calculate the average intra_row scale
    for point in nearest_dist:
        scale_intra += point[1]
    scale_intra /= len(nearest_dist)
    # print("Average scale: " + str(scale_intra))
    return scale_intra


