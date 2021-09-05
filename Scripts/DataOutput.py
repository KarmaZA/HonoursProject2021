# File to write the output of the program and to assemble it all in a single place
class DataOut:
    intra_spacing = 0
    inter_spacing = 0
    tree_count = 0
    image_angle = 0
    corner_tree_coords = []
    # ['pattern', correlation measure, count(?)]
    planting_patterns = []
    
    def __init__(self) -> None:
        pass

    def setIntra(intra):
        global intra_spacing
        intra_spacing = intra
        
        
    def setTreeCount(count):
        global tree_count
        tree_count = count
        
        
    def setAngle(angle):
        global image_angle
        image_angle = angle


    def writeDataToFile():
        print()
        print("The intra-spacing average is: " + str(intra_spacing))
        print("The Tree count detected is: " + str(tree_count))
        print("The angle of image is: " + str(image_angle))
        