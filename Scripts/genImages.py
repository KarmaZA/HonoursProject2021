# This file will hold the functions to deal with Image generation from the data read in
import numpy as np
import imageio

# References
    # https://www.agrihortieducation.com/2016/09/systems-of-planting.html
Template_Square = [[0,0],[0,1],[1,0],[1,1]]
  
"""This method draws polygons around the centroid given by the xy coordinate
Returns an Image Matrix with the drawn"""
def drawGuassianNoise(x,y, ImageToGen):
    # offset x and y so middle stays bright
    x -= 3
    y -= 3 
    for count_x in range(7):
            for count_y in range(7):
                ImageToGen[x+count_x][y+count_y][0:3] = 0
                # if (count_y == 1) and (count_x == 1):
                #     ImageToGen[x+count_x][y+count_y][0:3] = 0
                # else:
                #     if(ImageToGen[x+count_x][y+count_y][0] != 0):
                #         ImageToGen[x+count_x][y+count_y][0:3] = 128                  
    return ImageToGen

def SetBackground(template):
    height, width, depth = template.shape
    # template[0:width][0:height][0:depth] = 255
    for x in range(width):
        for y in range(height):
            template[y][x][0:3] = 255
    return template

"""Generates all the templates for Template Matching at the scaleds given in the length_array
returns the number of templates for Double Hedge and Rectangle. Other templates number == len(length_array)"""
def genAllTemplate(length_array):
    genSquareTemplate(length_array)
    genQuincunxTemplate(length_array)
    genEquilateralTriangleTemplate(length_array)
    genIsoscelesTriangleTemplate(length_array)
    genRectangleTemplate(length_array)
    return genDoubleHedgeTemplate(length_array)
 
"""Generates a square template for every length in the length array
All images are saved as TemplateSquareX.png 
where x is the position of the scale in the length array"""    
def genSquareTemplate(length_array):
    count = 0
    for length in length_array:
        print('Generating Square template with a length of: ' + str(length))
        template_size = length + 16

        TemplateToGen = np.zeros(shape=[template_size,template_size,3], dtype=np.uint8)
        TemplateToGen = SetBackground(TemplateToGen)
        for Template_Points in Template_Square:
            x = 5 + Template_Points[0] * length + (5*Template_Points[0])
            y = 5 + Template_Points[1] * length + (5*Template_Points[1])
            drawGuassianNoise(x, y, TemplateToGen)
        file_name = 'Images/TemplateSquare' + str(count) + '.png'
        imageio.imsave(file_name, TemplateToGen)
        count += 1
    
"""Generates a Qunicunx template for every length in the length array
The template is a square with a point in the center
All images are saved as TemplateQuincunxX.png 
where x is the position of the scale in the length array"""      
def genQuincunxTemplate(length_array):
    count = 0
    for length in length_array:
        print('Generating Quincunx template with a length of: ' + str(length))
        template_size = length + 13

        TemplateToGen = np.zeros(shape=[template_size,template_size,3], dtype=np.uint8)
        TemplateToGen = SetBackground(TemplateToGen)
        for Template_Points in Template_Square:
            x = 5 + Template_Points[0] * length
            y = 5 + Template_Points[1] * length
            drawGuassianNoise(x, y, TemplateToGen)
        
        x = 5 + int(0.5 * length)
        y = 5 + int(0.5 * length)
        drawGuassianNoise(x, y, TemplateToGen)
        file_name = 'Images/TemplateQuincunx' + str(count) + '.png'
        imageio.imsave(file_name, TemplateToGen)
        count += 1

    

"""Generates the Isosceles triangle template which is used to determine the Triangle planting pattern
Not to be confused with equilateral triangle which is used for Hexagonal pattern
All images are saved as TemplateTriangleX.png 
where x is the position of the scale in the length array"""
def genIsoscelesTriangleTemplate(length_array):
    count = 0
    for length in length_array:
        template_size = (length) + 3
        TemplateToGen = np.zeros(shape=[template_size,length+3,3], dtype=np.uint8)
        TemplateToGen = SetBackground(TemplateToGen)
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
        
"""Generates the Equilateral triangle template which is used to determine the Hexagonal pattern
Not to be confused with Isosceles triangle which is used for Triangle planting pattern
All images are saved as TemplateEquilateralTriangleX.png 
where x is the position of the scale in the length array"""    
def genEquilateralTriangleTemplate(length_array):
    count = 0
    template_triangle = [(0,0), (1,0), (0.5,0.86)]
    
    for length in length_array:
        print('Generating Equalateral Triangle template with a side length of ' + str(length))
        template_size = length + 3

        TemplateToGen = np.zeros(shape=[length+3,length+3,3], dtype=np.uint8)
        TemplateToGen = SetBackground(TemplateToGen)
        for pt in template_triangle:
            x = 1 + int(pt[0] * length)
            y = 1 + int(pt[1] * length)
            drawGuassianNoise(x, y, TemplateToGen)
        file_name = 'Images/TemplateEquilateralTriangle' + str(count) + '.png'
        imageio.imsave(file_name, TemplateToGen)
        count += 1
        

"""Generates a Rectangle template for every combination of 2 lengths in the length array
The width is the longer side in this case
All images are saved as TemplateRectangleX.png 
where x is the position of the scale in the length array"""      
def genRectangleTemplate(array_length):
    bFlag = False
    if len(array_length) == 1:
        array_length.append(int(array_length[0]*0.5))
        bFlag = True
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
            TemplateToGen = SetBackground(TemplateToGen)
            for Template_Points in Template_Square:
                x = 1 + Template_Points[0] * Height
                y = 1 + Template_Points[1] * Width
                drawGuassianNoise(x, y, TemplateToGen)
            
            file_name = 'Images/TemplateRectangle' + str(count) + '.png'
            imageio.imsave(file_name, TemplateToGen)
            count += 1
            height_count += 1
        width_count -= 1
    if bFlag:
        array_length.pop(1)
 
 
"""Generates a Double Hedge Row template for every combination of 2 lengths in the length array
The pattern goes Point -> Shorter distance -> Point -> Longer distance -> Point -> Shorter distance -> Point
All images are saved as TemplateDoubleHedgeX.png 
where x is the position of the scale in the length array"""      
def genDoubleHedgeTemplate(array_length):
    bFlag = False
    if len(array_length) == 1:
        array_length.append(int(array_length[0]*0.5))
        bFlag = True
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
            TemplateToGen = SetBackground(TemplateToGen)
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
    if bFlag:
        array_length.pop(1)
    return count