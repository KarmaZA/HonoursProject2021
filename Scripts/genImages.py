# This file will hold the functions to deal with Image generation from the data read in

import PIL

def genImageFromIdealisedData(PointSet):
    width = 400
    height = 300
    
    img = PIL.Image.new(mode="RGB", size=(width,height), color=0)
    # img.effect_noise(3,0)
    print("Show Image")
    img.show()
    print("Draw on")
    draw = PIL.ImageDraw.Draw(img)
    
    for point in PointSet:
        draw.point((point.x,point.y))
    
    draw.save("test.png")