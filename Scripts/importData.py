# File for importing the Data from files
# Also will be used for creating and manipulating data structures
from logging import error
import geopandas as gpd
import matplotlib.pyplot as plt
import json
import cv2


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
            file_name = 'Images/' + str(file_name) + str(x) + '.png'
            image_load = cv2.imread(file_name, 0)
                
            print("Images loaded.")
            image.append(image_load)
        return image
    
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