# This file will hold the functions to deal with Image generation from the data read in

import numpy as np
import imageio

square_length = 1
rectangle_height = 1
rectangle_width = 1
triangle_length = 1

# References
    # https://www.agrihortieducation.com/2016/09/systems-of-planting.html
Template_Square = [[0,0],[0,1],[1,0],[1,1]]

def genImageIdealised(PointSet):
    width = 0
    height = 0
    offset= 15
    for point in PointSet:
        if point.y > width:
            width = int(point.y)
            
        if point.x > height:
            height = int(point.x)   
        
    width *= 10 # Magic number?
    height *= 10 # Magic number?
    width += (2*offset)
    height += (offset*2)
    nrChannels = 3
    
    ImageToGen = np.zeros(shape=[height, width, nrChannels], dtype=np.uint8)
    imageio.imsave('Images/MainImage.png', ImageToGen)

    imageArray = imageio.imread('Images/MainImage.png')  
    # Insert distance calculation or number assignment
    for point in PointSet:
        x = offset + int(point.x*10)
        y = offset + int(point.y*10)
        # print(x, y)
        drawGuassianNoise(x,y,ImageToGen)
              
    imageio.imsave('Images/MainImage.png', ImageToGen)
    # Generate Templates
    CalcScale(PointSet)
    genAllTemplates()
    

def drawGuassianNoise(x,y, ImageToGen):
    # offset x and y so middle stays bright
    x -= 1
    y -= 1 
    for count_x in range(3):
            for count_y in range(3):
                if (count_y == 1) and (count_x == 1):
                    ImageToGen[x+count_x][y+count_y][0:3] = 255
                else:
                    ImageToGen[x+count_x][y+count_y][0:3] = 128
                    
    return ImageToGen
    

def genAllTemplates():
    genSquareTemplate(square_length)
    genQuincunxTemplate(square_length) # Qunicunx pattern is the square with a point in the center as well
    genRectangleTemplate(rectangle_width,rectangle_height)
    genIsoscelesTriangleTemplate(triangle_length)
    genEquilateralTriangleTemplate(triangle_length)
    genDoubleHedgeTemplate(rectangle_width, rectangle_height)
    genLineTemplate(triangle_length)
    

def CalcScale(PointSet):
    global square_length
    global rectangle_height
    global rectangle_width
    global triangle_length
    # Sum the points together on a y scale and a x scale
    # calc distance on each scale
    sum_x_array = []
    sum_y_array = []
    #Find min x and y
    min_x = 100
    min_y = 100
    for point in PointSet:
        if(min_x > point.x):
            min_x = int(point.x)
        if(min_y > point.y):
            min_y = int(point.y)
    for point in PointSet:
        if (point.x == min_x):
            sum_x_array.append(int(point.x+point.y))
        if (point.y == min_y):
            sum_y_array.append(int(point.x+point.y))
         
    #TODO
    #REWRITE this into the average difference of the arrays
    min_x = (sum_x_array[1] - sum_x_array[0]) * 10
    min_y = (sum_y_array[1] - sum_y_array[0]) * 10
    print()
    #print(sum_x_array, sum_y_array)
    print('The Square Pattern side length is ' + str(int((min_x+min_y)/2)))
    square_length = int((min_x+min_y)/2)

    if min_y != min_x:
        print('The Rectangle Pattern side length is: ' + str(min_y) + ' and ' + str(min_x))
    else:
        min_y += int(0.5*min_x)
        min_x = int(min_x*0.5)
        print("Width and height are equal. Likely output is a square pattern. Changing rectangle dimensions to avoid complications.")
        ################################## Maybe find a way to not use the template instead
    rectangle_height = min_y
    rectangle_width = min_x
    
    print('The length used for the triangle template is: ' + str(min(min_x,min_y)))
    triangle_length = min(min_x,min_y)
    
    
def genSquareTemplate(length):
    print('Generating Square template with a length of: ' + str(length))
    template_size = length + 3
    # Size = length of the side plus a pixel on each end
    TemplateToGen = np.zeros(shape=[template_size,template_size,3], dtype=np.uint8)
    for Template_Points in Template_Square:
        x = 1 + Template_Points[0] * length
        y = 1 + Template_Points[1] * length
        drawGuassianNoise(x, y, TemplateToGen)
        
    imageio.imsave('Images/TemplateSquare.png', TemplateToGen)
    
    
# Width should be the longer size for the sake of the program     
def genRectangleTemplate(Height, Width):
    if Width < Height:
        x = Width
        Width = Height
        Height = x
    print('Generating Rectangle template with a Height of: ' + str(Height) + ' and a width of : ' + str(Width))
    TemplateToGen = np.zeros(shape=[(Height + 3),(Width + 3),3], dtype=np.uint8)
    for Template_Points in Template_Square:
        x = 1 + Template_Points[0] * Height
        y = 1 + Template_Points[1] * Width
        drawGuassianNoise(x, y, TemplateToGen)
        
    imageio.imsave('Images/TemplateRectangle.png', TemplateToGen)
    
    
def genIsoscelesTriangleTemplate(length):
    if(length == 0):
        length = square_length
    print('Generating Triangle template with using a length of: ' + str(length))
    template_size = (length) + 3
    TemplateToGen = np.zeros(shape=[template_size,length+3,3], dtype=np.uint8)
    # Point 1
    y = 1 + Template_Square[0][0] * length
    x = 1 + Template_Square[0][1] * length
    # print(y,x)
    drawGuassianNoise(x, y, TemplateToGen)
    # Point 2
    y = 1 + Template_Square[1][0] * length
    x = 1 + Template_Square[1][1] * length
    # print(y,x)
    drawGuassianNoise(x, y, TemplateToGen)
    # Point 3
    y = 1 + Template_Square[2][0] * length
    x = 1 + int(0.5 * length)
    drawGuassianNoise(x, y, TemplateToGen)
    # print(y,x)
    drawGuassianNoise(x, y, TemplateToGen)
        
    imageio.imsave('Images/TemplateTriangle.png', TemplateToGen)
    
    
def genQuincunxTemplate(length):
    print('Generating Quincunx template with a length of: ' + str(length))
    template_size = length + 3
    # Size = length of the side plus a pixel on each end
    TemplateToGen = np.zeros(shape=[template_size,template_size,3], dtype=np.uint8)
    for Template_Points in Template_Square:
        x = 1 + Template_Points[0] * length
        y = 1 + Template_Points[1] * length
        drawGuassianNoise(x, y, TemplateToGen)
    
    x = 1 + int(0.5 * length)
    y = 1 + int(0.5 * length)
    drawGuassianNoise(x, y, TemplateToGen)
        
    imageio.imsave('Images/TemplateQuincunx.png', TemplateToGen)
    

def genEquilateralTriangleTemplate(length):
    template_triangle = [(0,0), (1,0), (0.5,0.86)]
    print('Generating Equalateral Triangle template with a side length of ' + str(length))
    
    TemplateToGen = np.zeros(shape=[length+3,length+3,3], dtype=np.uint8)
    for pt in template_triangle:
        x = 1 + int(pt[0] * length)
        y = 1 + int(pt[1] * length)
        drawGuassianNoise(x, y, TemplateToGen)
        
    imageio.imsave('Images/TemplateEquilateralTriangle.png', TemplateToGen)
    
    
def genDoubleHedgeTemplate(min_length, max_length):
    size = min_length + max_length + 3 + min_length
    
    TemplateToGen = np.zeros(shape=[7,size,3], dtype=np.uint8)
    
    size = 1
    drawGuassianNoise(3, size, TemplateToGen) # First point
    size += min_length
    drawGuassianNoise(3, size, TemplateToGen) # First point
    size += max_length
    drawGuassianNoise(3, size, TemplateToGen) # First point
    size += min_length
    drawGuassianNoise(3, size, TemplateToGen) # First point
    
    imageio.imsave('Images/TemplateDoubleHedge.png', TemplateToGen)
    
    
# line template for rotation calculation
def genLineTemplate(length):
    print('Generating line template for rotation')
    TemplateToGen = np.zeros(shape=[(length*4)+3,length+3,3], dtype=np.uint8)
    for k in range(4):
        x = 1 + (k*length)
        y = 1 + int(length/2)
        drawGuassianNoise(x, y, TemplateToGen)
        
    imageio.imsave('Images/TemplateLine.png', TemplateToGen)
    