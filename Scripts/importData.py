from logging import error
import re
import geopandas as gpd
import matplotlib.pyplot as plt
import json
import cv2

from shapely.geometry.multipoint import MultiPoint
from shapely.geometry.multipolygon import MultiPolygon
from shapely.geometry.point import Point
from shapely.geometry.polygon import Polygon

# Using Geopandas as it is updated more frequently
def importGeoPandasJSon(filename):
    try:
        with open(filename) as f:
        #data is a pandas.dataframe variable type
            data = gpd.read_file(f)     
        #print(data)
        return data
    except:
        print("File not found")
        return error
    
def loadImageFromFile(file_name, display_image_on_load, count):
    if count == 0:
        print("Loading the image file.")
        file_name = 'Images/' + str(file_name)
        image = cv2.imread(file_name, 0)
        if not image.any():
            print("Error image not loaded")

        if display_image_on_load:
            cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
            window_show_sized = cv2.resize(image, (960, 540))
            cv2.imshow("Image", window_show_sized)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        print("Image loaded.")
        return image
    else:
        image = []
        for x in range(count):
            print("Loading the image file.")
            load_file_name = 'Images/' + str(file_name) + str(x) + '.png'
            image_load = cv2.imread(load_file_name, 0)
                
            print("Images loaded.")
            image.append(image_load)
        return image
    
def importIdealisedData(filename):
    with open("Data/IdealData/" + filename) as dataFile:
        point_set = []
        for line in dataFile:
            coords = line.split()
            x = float(coords[0])
            y = float(coords[1])
            point_set.append(Point(x,y))            
        return MultiPoint(point_set)
    
def importGeoJSonAsPoints(filename,threshold):
        with open(filename) as f:
        #data is a pandas.dataframe variable type
            features = json.load(f)["features"]
            point_set = []
            for feature in features:
                if feature['properties']['confidence'] > threshold:
                    polygon = feature['geometry']['coordinates'][0]
                    poly_length = len(polygon)
                    x = 0
                    y = 0
                    for coordinate in range(poly_length): # Sum coordinates
                        x += polygon[coordinate][0]
                        y += polygon[coordinate][1]
                    # Average out a single point
                    x /= poly_length
                    y /= poly_length
                    point_set.append(Point(x,y))
        return MultiPoint(point_set)
    

def importGeoJSonAsPolygons(filename,threshold):
        with open(filename) as f:
        #data is a pandas.dataframe variable type
            features = json.load(f)["features"]
            polygon_set = []
            for feature in features:
                if feature['properties']['confidence'] > threshold:
                    polygon = feature['geometry']['coordinates'][0]
                    poly_length = len(polygon)
                    pointSet = []
                    for coordinate in range(poly_length): # Sum coordinates
                        pointSet.append(Point(polygon[coordinate][0], polygon[coordinate][1]))
                    # Average out a single point
                    polygon_set.append(Polygon([p.x,p.y] for p in pointSet))
                    # print(polygon[coordinate][0])
        return MultiPolygon(polygon_set)
    
def convertPolygonsToCentroids(PolygonSet):
    PointSet = []
    for poly in PolygonSet:
        PointSet.append(Point(poly.centroid.coords))
    # for point in PointSet:
        # print(point.x, point.y)
    return MultiPoint(PointSet)
    
def displayPointSet(PointSet):
    # for points in PointSet:
    #     print(points)
        
    xs = [point.x for point in PointSet]
    ys = [point.y for point in PointSet]
    plt.scatter(xs,ys)
    plt.show()
    
def displayPolygonSet(PolygonSet):
    fig, axs = plt.subplots()
    axs.set_aspect('equal', 'datalim')

    for geom in PolygonSet.geoms:    
        xs, ys = geom.exterior.xy    
        axs.fill(xs, ys, alpha=0.5, fc='r', ec='none')

    plt.show()
    
def formatGeoJSONData(PointSet):
        #Calculate number of decimal points
    decimal_count = int(len(str(PointSet[0].x).split('.')[1]))
    decimal_count = 10**decimal_count
    print('The decimal count is ' + str(decimal_count))
    min_x, min_y = (200, 200)
    for point in PointSet:
        if min_x > point.x:
            min_x = point.x
        if min_y > point.y:
            min_y = point.y
            
    # min_x*=decimal_count
    # min_y*=decimal_count
    PointSet_to_return = []
    for point in PointSet:
        
        x = point.x - min_x
        x = point.x * decimal_count
        
        y = point.y - min_y
        y = point.y  * decimal_count
        print(x, y)
        PointSet_to_return.append(Point(x,y))
    return MultiPoint(PointSet_to_return)
        