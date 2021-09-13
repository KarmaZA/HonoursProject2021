# File to write the output of the program and to assemble it all in a single place
class DataOut:
    intra_spacing = 0
    inter_spacing = 0
    tree_count = 0
    image_angle = 0
    row_count = 0
    avg_tree_row = 0
    road_count = 0
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
        # min x, min y, max x, max y
        self.corner_tree_coords = CornerT

    def setRowNumbers(self, rownum):
        self.row_count = rownum

    def setTreesPerRow(self, TRcount):
        self.avg_tree_row = TRcount

    def setRoadCount(self, Rcount):
        road_count = Rcount

    def writeDataToFile(self):
        print()
        print("The intra-row spacing mean value is: " + str(self.intra_spacing))
        print("The inter-row spacing mean value is: " + str(self.inter_spacing))
        print("The Tree count detected is: " + str(self.tree_count))
        print("The number of rows detected is: " + str(row_count))
        print("The mean value per row is: " + str(avg_tree_row))
        print("There were " + str(road_count) + ' road(s) or distches detected')
        for point in corner_tree_coords:
            print("A corner coordinate is: " + str(point.x) + " , " + str(point.y))
        print("The detected patterns are " + patterns_list)
        # print("The angle of image is: " + str(self.image_angle))
        with open('outputFile.txt', 'w') as f:
            f.write("The intra-row spacing mean value is: " + str(self.intra_spacing))
            f.write("The inter-row spacing mean value is: " + str(self.inter_spacing))
            f.write("The Tree count detected is: " + str(self.tree_count))
            f.write("The number of rows detected is: " + str(row_count))
            f.write("The mean value per row is: " + str(avg_tree_row))
            f.write("There were " + str(road_count) + ' road(s) or distches detected')
            for point in corner_tree_coords:
                f.write("A corner coordinate is: " + str(point.x) + " , " + str(point.y))
            f.write("The detected patterns are " + patterns_list)

        print("Data written to outputFile.txt")

        
        