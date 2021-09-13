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

def countRowNumbers(pointSet, angle):
    row_count = 0
    inter_spacing = 0

    return (row_count, inter_spacing)


def meanRowCount(PointSet)
    meanCount = 0
    #THIS SHOULD PROBABLY BE DONE DURING DETECTION
    return meanCount


