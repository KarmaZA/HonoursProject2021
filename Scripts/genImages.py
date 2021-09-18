# This file will hold the functions to deal with Image generation from the data read in
import numpy as np
import imageio


# References
    # https://www.agrihortieducation.com/2016/09/systems-of-planting.html
Template_Square = [[0,0],[0,1],[1,0],[1,1]]
# template_size = []

point_array = [255,255,255,0,0,0,255,255,255],[255,255,0,0,0,0,255,255,255],[255,0,0,0,0,0,0,255,255],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[255,255,0,0,0,0,0,255,255],[255,255,255,0,0,0,255,255,255],[255,255,255,0,0,0,255,255,255]  
"""This method draws polygons around the centroid given by the xy coordinate
Returns an Image Matrix with the drawn"""
def drawGuassianNoise(x,y, ImageToGen):
    # offset x and y so middle stays bright
    x -= 3
    y -= 3 
    for count_x in range(9):
            for count_y in range(9):
                ImageToGen[x+count_x][y+count_y] = point_array[count_x][count_y]
                                
    return ImageToGen

def SetBackground(template):
    height, width = template.shape
    for x in range(width):
        for y in range(height):
            template[y][x] = 255
    return template

"""Generates all the templates for Template Matching at the scaleds given in the length_array
returns the number of templates for Double Hedge and Rectangle. Other templates number == len(length_array)"""
def genAllTemplate(len_x, len_y, length_array):
    # global template_size
    # height = max(len_x) + 14
    # width = max(len_y) + 14
    # print("SD")
    # #len_y is smaller
    # template_size = [ height, width]

    genSquareTemplate(length_array)
    genQuincunxTemplate(length_array)
    genEquilateralTriangleTemplate(length_array)
    genIsoscelesTriangleTemplate(len_x, len_y)
    genRectangleTemplate(len_x, len_y)
    return genDoubleHedgeTemplate(len_x, len_y)
 
"""Generates a square template for every length in the length array
All images are saved as TemplateSquareX.png 
where x is the position of the scale in the length array"""    
def genSquareTemplate(length_array):
    count = 0
    for length in length_array:
        # print('Generating Square template with a length of: ' + str(length))
        template_size = length + 14 #Magic number 

        TemplateToGen = np.zeros(shape=[template_size,template_size], dtype=np.uint8)
        TemplateToGen = SetBackground(TemplateToGen)
        for Template_Points in Template_Square:
            x = 5 + Template_Points[0] * length
            y = 5 + Template_Points[1] * length
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
        # print('Generating Quincunx template with a length of: ' + str(length))
        template_size = length * 2 + 13

        TemplateToGen = np.zeros(shape=[template_size,template_size], dtype=np.uint8)
        TemplateToGen = SetBackground(TemplateToGen)

        #1
        x = 5
        y = 5 + length
        drawGuassianNoise(x, y, TemplateToGen)
        #2
        x += length
        drawGuassianNoise(x, y, TemplateToGen)
        #3
        x += length
        drawGuassianNoise(x, y, TemplateToGen)
        #4
        x -= length
        y += length
        drawGuassianNoise(x, y, TemplateToGen)
        #5
        y -= 2*length
        drawGuassianNoise(x, y, TemplateToGen)
        
        file_name = 'Images/TemplateQuincunx' + str(count) + '.png'
        imageio.imsave(file_name, TemplateToGen)
        count += 1


        
"""Generates the Equilateral triangle template which is used to determine the Hexagonal pattern
Not to be confused with Isosceles triangle which is used for Triangle planting pattern
All images are saved as TemplateEquilateralTriangleX.png 
where x is the position of the scale in the length array"""    
def genEquilateralTriangleTemplate(length_array):
    count = 0
    for length in length_array:
        template_size = (length) + 14
        TemplateToGen = np.zeros(shape=[template_size,length+14], dtype=np.uint8)
        TemplateToGen = SetBackground(TemplateToGen)
        y = 5
        x = 5
        # print(y,x)
        drawGuassianNoise(x, y, TemplateToGen)
        # Point 2
        y += length
        drawGuassianNoise(x, y, TemplateToGen)
        # Point 3
        x += length
        y -= int(0.5 * length)
        drawGuassianNoise(x, y, TemplateToGen)   
        file_name = 'Images/TemplateEquilateralTriangle' + str(count) + '.png'
        imageio.imsave(file_name, TemplateToGen)
        count += 1



"""Generates the Isosceles triangle template which is used to determine the Triangle planting pattern
Not to be confused with equilateral triangle which is used for Hexagonal pattern
All images are saved as TemplateTriangleX.png 
where x is the position of the scale in the length array"""
#Template_Square = [[0,0],[0,1],[1,0],[1,1]]
def genIsoscelesTriangleTemplate(len_x, len_y):
    count = 0
    for length in len_x:
        for width in len_y:
            if length > 1.5*width:
                template_size = (length) + 14
                TemplateToGen = np.zeros(shape=[template_size,length+14], dtype=np.uint8)
                TemplateToGen = SetBackground(TemplateToGen)
                y = 5
                x = 5
                # print(y,x)
                drawGuassianNoise(x, y, TemplateToGen)
                # Point 2
                y += width
                drawGuassianNoise(x, y, TemplateToGen)
                # Point 3
                x += length
                y -= int(0.5 * width)
                drawGuassianNoise(x, y, TemplateToGen)
                # drawGuassianNoise(x, y, TemplateToGen)
                file_name = 'Images/TemplateTriangle' + str(count) + '.png'
                imageio.imsave(file_name, TemplateToGen)
                count += 1
    if count == 0:       
        width = len_x[0]
        length = width*2
        template_size = (length) + 14
        TemplateToGen = np.zeros(shape=[template_size,length+14], dtype=np.uint8)
        TemplateToGen = SetBackground(TemplateToGen)
        y = 5
        x = 5
        # print(y,x)
        drawGuassianNoise(x, y, TemplateToGen)
        # Point 2
        y += length
        drawGuassianNoise(x, y, TemplateToGen)
        # Point 3
        x += width
        y -= int(0.5 * length)
        drawGuassianNoise(x, y, TemplateToGen)
        # drawGuassianNoise(x, y, TemplateToGen)
        file_name = 'Images/TemplateTriangle' + str(count) + '.png'
        imageio.imsave(file_name, TemplateToGen)
        count += 1
            

"""Generates a Rectangle template for every combination of 2 lengths in the length array
The width is the longer side in this case
All images are saved as TemplateRectangleX.png 
where x is the position of the scale in the length array"""      
def genRectangleTemplate(len_x, len_y):
    count = 0
    for Height in len_x:
        for Width in len_y:
            if Height > 1.5*Width:
                # Gen the rectangle
                # print('Generating Rectangle template with a Height of: ' + str(Height) + ' and a width of : ' + str(Width))
                TemplateToGen = np.zeros(shape=[(Height + 14),(Width + 14)], dtype=np.uint8)
                TemplateToGen = SetBackground(TemplateToGen)
                for Template_Points in Template_Square:
                    x = 5 + Template_Points[0] * Height
                    y = 5 + Template_Points[1] * Width
                    drawGuassianNoise(x, y, TemplateToGen)
                
                file_name = 'Images/TemplateRectangle' + str(count) + '.png'
                imageio.imsave(file_name, TemplateToGen)
                count += 1

    if count == 0:
        Width = len_y[0]
        Height = Width*2
        TemplateToGen = np.zeros(shape=[(Height + 14),(Width + 14)], dtype=np.uint8)
        TemplateToGen = SetBackground(TemplateToGen)
        for Template_Points in Template_Square:
            x = 5 + Template_Points[0] * Height
            y = 5 + Template_Points[1] * Width
            drawGuassianNoise(x, y, TemplateToGen)
        
        file_name = 'Images/TemplateRectangle' + str(count) + '.png'
        imageio.imsave(file_name, TemplateToGen)
        count += 1
 
 
"""Generates a Double Hedge Row template for every combination of 2 lengths in the length array
The pattern goes Point -> Shorter distance -> Point -> Longer distance -> Point -> Shorter distance -> Point
All images are saved as TemplateDoubleHedgeX.png 
where x is the position of the scale in the length array"""      
def genDoubleHedgeTemplate(len_x, len_y):
    count = 0
    for Height in len_x:
        for Width in len_y:
            if Height > 1.5*Width:
                min_length = Width
                max_length = Height
                # Gen the rectangle
                # print('Generating Hedge Row template with a intra spacing of: ' + str(min_length) + ' and a inter spacing of: ' + str(max_length))
                size = min_length + max_length + 14 + min_length
        
                TemplateToGen = np.zeros(shape=[11,size], dtype=np.uint8)
                TemplateToGen = SetBackground(TemplateToGen)
                size = 5
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

    if count == 0:
        min_length = Width
        max_length = min_length * 2
        # Gen the rectangle
        # print('Generating Hedge Row template with a intra spacing of: ' + str(min_length) + ' and a inter spacing of: ' + str(max_length))
        size = min_length + max_length + 14 + min_length

        TemplateToGen = np.zeros(shape=[11,size], dtype=np.uint8)
        TemplateToGen = SetBackground(TemplateToGen)
        size = 5
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
    return count