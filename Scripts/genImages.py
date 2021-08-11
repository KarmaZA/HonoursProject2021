# This file will hold the functions to deal with Image generation from the data read in

import numpy as np
import imageio


Template_Square = [[0,0],[0,1],[1,0],[1,1]]

def genImageIdealised(PointSet):
    width = 768
    height = 768
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
        
    imageio.imsave('MainImage.png', ImageToGen)
    
    # Generate Template
    genSquareTemplate(30)
    genRectangleTemplate(60,30)
    genTriangleTemplate(40)
    
    
def genSquareTemplate(length):
    template_size = length + 3
    # Size = length of the side plus a pixel on each end
    TemplateToGen = np.zeros(shape=[template_size,template_size,3], dtype=np.uint8)
    for Template_Points in Template_Square:
        x = 1 + Template_Points[0] * length
        y = 1 + Template_Points[1] * length
        TemplateToGen[x][y][0:3] = 255
        
    imageio.imsave('TemplateSquare.png', TemplateToGen)
    
    
# Width should be the longer size for the sake of the program     
def genRectangleTemplate(Height, Width):
    
    TemplateToGen = np.zeros(shape=[(Height + 3),(Width + 3),3], dtype=np.uint8)
    for Template_Points in Template_Square:
        x = 1 + Template_Points[0] * Height
        y = 1 + Template_Points[1] * Width
        TemplateToGen[x][y][0:3] = 255
        
    imageio.imsave('TemplateRectangle.png', TemplateToGen)
    
    
def genTriangleTemplate(length):
    template_size = (length) + 3
    TemplateToGen = np.zeros(shape=[template_size,length+3,3], dtype=np.uint8)
    # Point 1
    y = 1 + Template_Square[0][0] * length
    x = 1 + Template_Square[0][1] * length
    print(y,x)
    TemplateToGen[x][y][0:3] = 255
    # Point 2
    y = 1 + Template_Square[1][0] * length
    x = 1 + Template_Square[1][1] * length
    print(y,x)
    TemplateToGen[x][y][0:3] = 255
    # Point 3
    y = 1 + Template_Square[2][0] * length
    x = 1 + int(0.5 * length)
    TemplateToGen[x][y][0:3] = 255
    print(y,x)
    TemplateToGen[x][y][0:3] = 255
        
    imageio.imsave('TemplateTriangle.png', TemplateToGen)