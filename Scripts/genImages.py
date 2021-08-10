# This file will hold the functions to deal with Image generation from the data read in

import numpy as np
import imageio


Template_Square = [[0,0],[0,1],[1,0],[1,1]]

def genImageIdealised(PointSet):
    width = 512
    height = 512
    nrChannels = 3
    ImageToGen = np.zeros(shape=[height, width, nrChannels], dtype=np.uint8)
    imageio.imsave('MainImage.png', ImageToGen)
    
    imageArray = imageio.imread('MainImage.png')
    print(type(imageArray))
    print(ImageToGen.shape, ImageToGen.dtype)
    
    # Create a .raw file for the image
    ImageToGen.tofile('MainImage.raw')
    
    # Insert distance calculation or number assignment
    
    offset = 15
    for point in PointSet:
        x = offset + int(point.x*10)
        y = offset + int(point.y*10)
        print(x, y)
        ImageToGen[x][y][0:3] = 255
        #ImageToGen[point.x*10][point.y+10][1] = 255
        #ImageToGen[point.x*10][point.y+10][2] = 255
        
    imageio.imsave('MainImage.png', ImageToGen)
    
    # Generate Template
    # Currently Set for the Square Template
    TemplateToGen = np.zeros(shape=[33,33,3], dtype=np.uint8)
    for Template_Points in Template_Square:
        x = 1 + Template_Points[0] * 30
        y = 1 + Template_Points[1] * 30
        TemplateToGen[x][y][0:3] = 255
        
    imageio.imsave('TemplateImage.png', TemplateToGen)
    