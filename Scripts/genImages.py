# This file will hold the functions to deal with Image generation from the data read in

import numpy as np
import imageio

def genImageIdealised(PointSet):
    width = 400
    height = 300
    nrChannels = 3
    ImageToGen = np.zeros(shape=[height, width, nrChannels], dtype=np.uint8)
    imageio.imsave('template.png', ImageToGen)
    
    imageArray = imageio.imread('template.png')
    print(type(imageArray))
    print(ImageToGen.shape, ImageToGen.dtype)
    
    # Create a .raw file for the image
    ImageToGen.tofile('template.raw')
    
    # Insert distance calculation or number assignment
    
    offset = 15
    for point in PointSet:
        x = offset + int(point.x*10)
        y = offset + int(point.y*10)
        print(x, y)
        ImageToGen[x][y][0:3] = 255
        #ImageToGen[point.x*10][point.y+10][1] = 255
        #ImageToGen[point.x*10][point.y+10][2] = 255
        
    imageio.imsave('template.png', ImageToGen)
    