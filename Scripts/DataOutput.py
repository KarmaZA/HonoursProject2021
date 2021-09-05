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


    def setIntra(self, intra):
        self.intra_spacing = intra
        
        
    def setTreeCount(self, count):
        global tree_count
        self.tree_count = count
        
        
    def setAngle(self, angle):
        self.image_angle = angle
        
    
    ######################Unused    
    def setInter(self, inte):
        self.inter_spacing = inte


    def setPatterns(self, patterns_list):
        self.planting_patterns = patterns_list
        
        
    def setCorner(self, CornerT):
        self.corner_tree_coords = CornerT


    def writeDataToFile():
        print()
        print("The intra-spacing average is: " + str(intra_spacing))
        print("The Tree count detected is: " + str(tree_count))
        print("The angle of image is: " + str(image_angle))
        