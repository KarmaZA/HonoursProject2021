# This class will take input of the pointset and calculate the rotation of the image
import SimilarityMeasures as SM

import cv2
import imutils
from scipy.spatial import distance
from sklearn.neighbors import KDTree
import numpy as np

def calcImageRotation(Pointset):
    rotation = 0 # Degrees
    image = cv2.imread('Images/TemplateLine.png', 0)
    main_image = cv2.imread('Images/MainImage.png', 0)
    rotation_correlation_list = []
    # Only need to rotate 180 degrees
    for x in range(8):
        rotated = imutils.rotate(image,angle=(x*45))
        correlation_measure = SM.templateMatching_correlation_score(main_image, image)
        rotation_correlation_list.append(correlation_measure)
        #window_show_sized = cv2.resize(rotated, (960, 540));
        #cv2.imshow("Matched image", window_show_sized)
        #cv2.waitKey()
        #cv2.destroyAllWindows()
        
    print("The correlation list is")
    print(rotation_correlation_list)
    
    
    #Calc Scale will return an array of mean distances. These could number from 1 to several
def CalcScale(PointSet):
    distance_to_return = []  
    
    # https://stackoverflow.com/questions/48126771/nearest-neighbour-search-kdtree/48127117#48127117
    dataset = KDTree(PointSet)
    nearest_dist, nearest_ind = dataset.query(PointSet, k=4)
    print(dataset)
    print(nearest_dist[:, 1:5])
    print(nearest_ind[:, 1])
    
    # Change to random point checking than O(n2)
    for x in range(len(PointSet)):
        for y in range(3):
            if not nearest_dist[x,y+1] in distance_to_return:
                distance_to_return.append(np.round(nearest_dist[x,y+1],2)) #ROUND DISTANCE TO 2 FLOATING POINTS
                print(nearest_dist[x,y+1])
            
    return distance_to_return


