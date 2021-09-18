# A file for calculating the parameters to be extracted from the data

from LinkedList import LinkedList, Node
from sklearn.neighbors import KDTree
from shapely.geometry import Point

import matplotlib.pyplot as plt
import DataCalculations
import random

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
    max_row_count = 0
    inter_spacing = 0
    spacing_list = []
    point_list = []
    angle_perp_1 = (angle + 90)
    angle_perp_2 = (angle - 90)
    print(angle, angle_perp_1, angle_perp_2)
    nearest_dist, nearest_ind = dataset.query(PointSet, k=8)

    for z in range(10):
        row_count = 0
        spacing_list = []
        point_list = []

        # spacing_list
        row_count += 1

        count_rows = True
        point_list.append(random.randint(0, len(PointSet)-1))
        while count_rows:
            count_rows = False
            for x in range(8):
                if not (nearest_ind[point_list[-1]][x] in  point_list):
                    angle_check = DataCalculations.calcLineRotation(PointSet[nearest_ind[point_list[-1]][0]],PointSet[nearest_ind[point_list[-1]][x]])
                    if DataCalculations.AnglesInRange(angle_perp_1, angle_check, 23):
                        row_count += 1
                        point_list.append(nearest_ind[point_list[-1]][x])
                        spacing_list.append(nearest_dist[point_list[-1]][x])
                        count_rows = True
                        break

        # Count rows in opposite direction
        count_rows = True
        while count_rows:
            count_rows = False
            for x in range(8):
                # print("here")
                # print(angle_check, angle_perp_2)
                if not (nearest_ind[point_list[0]][x] in  point_list):
                    angle_check = DataCalculations.calcLineRotation(PointSet[nearest_ind[point_list[0]][0]],PointSet[nearest_ind[point_list[0]][x]])
                    if DataCalculations.AnglesInRange(angle_perp_2, angle_check, 23):
                        row_count += 1
                        point_list.insert(0, nearest_ind[point_list[0]][x])
                        spacing_list.append(nearest_dist[point_list[0]][x])
                        count_rows = True
                        break
        if row_count > max_row_count:
            # Reset road count because a road would be present in whole dataset
            road_count = 0
            if len(spacing_list) > 0:
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


def calcScaleIntra(PointSet, dataset):
    nearest_dist, nearest_ind = dataset.query(PointSet, k=4)
    scale_intra = 0   
    #Calculate the average intra_row scale
    for point in nearest_dist:
        scale_intra += point[1]
    scale_intra /= len(nearest_dist)
    # print("Average scale: " + str(scale_intra))
    return scale_intra

def calcScaleInter(PointSet, angle):
    dataset = KDTree(PointSet)
    nearest_dist, nearest_ind = dataset.query(PointSet, k=10) #high k to account for noise
    inter_list = []
    angle_list = []
    for i in range(len(nearest_ind)):
        for j in range(10):
            angle_curr = DataCalculations.calcLineRotation(PointSet[nearest_ind[i][0]], PointSet[nearest_ind[i][j]])
            angle_curr = angle_curr - angle
            # print(angle_curr, angle)
            angle_curr = angle_curr % 180
            # print(angle_curr)
            if DataCalculations.AnglesInRange(angle_curr,90,10) or DataCalculations.AnglesInRange(angle_curr,60,10):
                inter_list.append(nearest_dist[i][j])
                angle_list.append(DataCalculations.calcLineRotation(PointSet[nearest_ind[i][0]], PointSet[nearest_ind[i][j]]))
                break

    inter_val = 0
    for spac in inter_list:
        inter_val += spac
    inter_val /= len(inter_list)
    angle_curr = DataCalculations.AverageAngle(angle_list)
    print('out')
    print(inter_val, angle_curr)
    return (inter_val, angle_curr)

def appAngleRange(angle):
    testAngles = [0,23,45,67,90,112,135,167]
    angle = angle % 90
    if angle > 45:
        angle = abs(angle - 90)
    for x in range(8):
        testAngles[x] += angle
    return testAngles
