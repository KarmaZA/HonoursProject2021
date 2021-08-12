# File for importing the Data from files
# Also will be used for creating and manipulating data structures
from logging import error
import geopandas as gpd
import matplotlib.pyplot as plt
import json


from shapely.geometry.multipoint import MultiPoint
from shapely.geometry.point import Point


# Using Geopandas as it is updated more frequently
def importGeoPandasJSon(filename):
    try:
        with open(filename) as f:
        #data is a pandas.dataframe variable type
            data = gpd.read_file(f)     
        # Note use of iterrows() to iterate   
        # for element, row in data.iterrows():
        #    print(element, row)
        #print(data)
        return data
    except:
        print("File not found")
        return error
    
    
### TODO 
    #AT READ IN CALC X AND Y MIN AND MAX
def importIdealisedData(filename):
    
    with open("Data/IdealData/" + filename) as dataFile:
        point_set = []
        for line in dataFile:
            coords = line.split()
            x = float(coords[0])
            y = float(coords[1])
            point_set.append(Point(x,y))            
        return MultiPoint(point_set)
    
def importGeoJSonAsPoints(filename):
        with open(filename) as f:
        #data is a pandas.dataframe variable type
            features = json.load(f)["features"]
            point_set = []
            for feature in features:
                if feature['properties']['confidence'] > 0.8:
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
    
def displayPointSet(PointSet):
    for points in PointSet:
        print(points)
        
    xs = [point.x for point in PointSet]
    ys = [point.y for point in PointSet]
    plt.scatter(xs,ys)
    plt.show()