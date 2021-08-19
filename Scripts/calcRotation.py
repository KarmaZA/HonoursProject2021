# This class will take input of the pointset and calculate the rotation of the image
import SimilarityMeasures as SM

import cv2
import imutils

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