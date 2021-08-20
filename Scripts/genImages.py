# This file will hold the functions to deal with Image generation from the data read in

import numpy as np
import imageio

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
    

def drawGuassianNoise(x,y, ImageToGen):
    # offset x and y so middle stays bright
    x -= 1
    y -= 1 
    for count_x in range(3):
            for count_y in range(3):
                if (count_y == 1) and (count_x == 1):
                    ImageToGen[x+count_x][y+count_y][0:3] = 255
                else:
                    if(ImageToGen[x+count_x][y+count_y][0] != 255):
                        ImageToGen[x+count_x][y+count_y][0:3] = 128
                    
    return ImageToGen

def genAllTemplate(length_array):
    genSquareTemplate(length_array)
    genQuincunxTemplate(length_array)
    genRectangleTemplate(length_array)
    genEquilateralTriangleTemplate(length_array)
    genIsoscelesTriangleTemplate(length_array)
    return genDoubleHedgeTemplate(length_array)
 
    
def genSquareTemplate(length_array):
    count = 0
    for length in length_array:
        print('Generating Square template with a length of: ' + str(length))
        template_size = length + 3

        TemplateToGen = np.zeros(shape=[template_size,template_size,3], dtype=np.uint8)
        for Template_Points in Template_Square:
            x = 1 + Template_Points[0] * length
            y = 1 + Template_Points[1] * length
            drawGuassianNoise(x, y, TemplateToGen)
        file_name = 'Images/TemplateSquare' + str(count) + '.png'
        imageio.imsave(file_name, TemplateToGen)
        count += 1
    
    
def genQuincunxTemplate(length_array):
    count = 0
    for length in length_array:
        print('Generating Quincunx template with a length of: ' + str(length))
        template_size = length + 3

        TemplateToGen = np.zeros(shape=[template_size,template_size,3], dtype=np.uint8)
        for Template_Points in Template_Square:
            x = 1 + Template_Points[0] * length
            y = 1 + Template_Points[1] * length
            drawGuassianNoise(x, y, TemplateToGen)
        
        x = 1 + int(0.5 * length)
        y = 1 + int(0.5 * length)
        drawGuassianNoise(x, y, TemplateToGen)
        file_name = 'Images/TemplateQuincunx' + str(count) + '.png'
        imageio.imsave(file_name, TemplateToGen)
        count += 1

    

    
def genIsoscelesTriangleTemplate(length_array):
    count = 0
    for length in length_array:
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
        file_name = 'Images/TemplateTriangle' + str(count) + '.png'
        imageio.imsave(file_name, TemplateToGen)
        count += 1
        
    
def genEquilateralTriangleTemplate(length_array):
    count = 0
    template_triangle = [(0,0), (1,0), (0.5,0.86)]
    
    for length in length_array:
        print('Generating Equalateral Triangle template with a side length of ' + str(length))
        template_size = length + 3

        TemplateToGen = np.zeros(shape=[length+3,length+3,3], dtype=np.uint8)
        for pt in template_triangle:
            x = 1 + int(pt[0] * length)
            y = 1 + int(pt[1] * length)
            drawGuassianNoise(x, y, TemplateToGen)
        file_name = 'Images/TemplateEquilateralTriangle' + str(count) + '.png'
        imageio.imsave(file_name, TemplateToGen)
        count += 1
        

# Width should be the longer size for the sake of the program     
def genRectangleTemplate(array_length):
    
    count = 0
    if len(array_length) == 1:
        Width = array_length[0]
        Height = 0.5 * array_length[0]
    width_count = len(array_length) - 1
    while width_count > 0:
        height_count = 0
        while height_count < width_count:
            Height = array_length[height_count]
            Width = array_length[width_count]
            # Gen the rectangle
            print('Generating Rectangle template with a Height of: ' + str(Height) + ' and a width of : ' + str(Width))
            TemplateToGen = np.zeros(shape=[(Height + 3),(Width + 3),3], dtype=np.uint8)
            for Template_Points in Template_Square:
                x = 1 + Template_Points[0] * Height
                y = 1 + Template_Points[1] * Width
                drawGuassianNoise(x, y, TemplateToGen)
            
            file_name = 'Images/TemplateRectangle' + str(count) + '.png'
            imageio.imsave(file_name, TemplateToGen)
            count += 1
            height_count += 1
        width_count -= 1
 
    
def genDoubleHedgeTemplate(array_length):
    count = 0
    if len(array_length) == 1:
        Width = array_length[0]
        Height = 0.5 * array_length[0]
    width_count = len(array_length) - 1
    while width_count > 0:
        height_count = 0
        while height_count < width_count:
            min_length = array_length[height_count]
            max_length = array_length[width_count]
            # Gen the rectangle
            print('Generating Hedge Row template with a intra spacing of: ' + str(min_length) + ' and a inter spacing of: ' + str(max_length))
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
            
            file_name = 'Images/TemplateDoubleHedge' + str(count) + '.png'
            imageio.imsave(file_name, TemplateToGen)
            count += 1
            height_count += 1
        width_count -= 1
    return count

    
# line template for rotation calculation
def genLineTemplate(length):
    print('Generating line template for rotation')
    TemplateToGen = np.zeros(shape=[(length*4)+3,length+3,3], dtype=np.uint8)
    for k in range(4):
        x = 1 + (k*length)
        y = 1 + int(length/2)
        drawGuassianNoise(x, y, TemplateToGen)
        
    imageio.imsave('Images/TemplateLine.png', TemplateToGen)
    
def genUnbrokenLine(length):
    print("Generating unbroken line")
    
    TemplateToGen = np.zeros(shape=[length+3,(length*5)+3,3], dtype=np.uint8)
    midPoint = int((length+3)/2)
    for k in range((length*5)+3):
        x = 1 + midPoint
        y = k
        TemplateToGen[x][y][0:3] = 255
        
        x = 2 + midPoint
        y = k
        TemplateToGen[x][y][0:3] = 192
        
        x = midPoint
        y = k
        TemplateToGen[x][y][0:3] = 192
        
        x = 3 + midPoint
        y = k
        TemplateToGen[x][y][0:3] = 128
        
        x = midPoint - 1
        y = k
        TemplateToGen[x][y][0:3] = 128
        
    imageio.imsave('Images/TemplateLineUnbroken.png', TemplateToGen)