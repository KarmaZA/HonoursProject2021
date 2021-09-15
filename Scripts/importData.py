import matplotlib.pyplot as plt
import json
import cv2

from shapely.geometry.multipoint import MultiPoint
from shapely.geometry.multipolygon import MultiPolygon
from shapely.geometry.point import Point
from shapely.geometry.polygon import Polygon
    
"""Loads images from the file. filename is the name of the image (or base name) and count is number of images with that name to be loaded
if count > 0 file naming format is filename + count + .png"""
def loadImageFromFile(file_name, count):
    if count == 0:
        # print("Loading the image file.")
        file_name = str(file_name)
        image = cv2.imread(file_name, 0)
        if not image.any():
            print("Error image not loaded")
        return image
    else:
        image = []
        for x in range(count):
            # print("Loading the image file.")
            load_file_name = 'Images/' + str(file_name) + str(x) + '.png'
            image_load = cv2.imread(load_file_name, 0)
                
            # print("Images loaded.")
            image.append(image_load)
        return image
    
"""Used to import idealised datafiles into the program as points to mimic geojson files"""
def importIdealisedData(filename):
    with open("Data/IdealData/" + filename) as dataFile:
        point_set = []
        for line in dataFile:
            coords = line.split()
            x = float(coords[0])
            y = float(coords[1])
            point_set.append(Point(x,y))            
        return MultiPoint(point_set)
    
"""Imports GeoJSON files into the program and dynamically calculates the centroid and returns that as a point which is a shapely.geometry object."""
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

"""Imports the whole polygons of a GeoJSON files into the program as a shapely.geometry object."""
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
    
"""If you have imported polygons into the system this will convert them into centroids saved as shapely.geometry.point."""
def convertPolygonsToCentroids(PolygonSet):
    PointSet = []
    for poly in PolygonSet:
        PointSet.append(Point(poly.centroid.coords))
    return MultiPoint(PointSet)
    
"""Display the shapely.geometry.MultiPoint data structure on a graph"""
def displayPointSet(PointSet):
    xs = [point.x for point in PointSet]
    ys = [point.y for point in PointSet]
    plt.scatter(xs,ys)
    plt.show()
    
"""Display the shapely.geometry.MultiPolygon data structure on a graph"""
def displayPolygonSet(PolygonSet):
    fig, axs = plt.subplots()
    axs.set_aspect('equal', 'datalim')
    for geom in PolygonSet.geoms:    
        xs, ys = geom.exterior.xy    
        axs.fill(xs, ys, alpha=0.5, fc='r', ec='none')
    plt.show()        