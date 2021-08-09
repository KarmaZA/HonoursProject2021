# This file will hold the functions to deal with Image generation from the data read in

from PIL import Image

def genImageFromIdealisedData():
    width = 400
    height = 300
    
    img = Image.new(mode="RGB", size=(width,height), color=0)
    img.show
    