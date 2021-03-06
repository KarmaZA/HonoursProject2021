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
    patterns = ''
    

    def __init__(self) -> None:
        pass

    def setIntra(self, intra):
        self.intra_spacing = intra        
        
    def setTreeCount(self, count):
        global tree_count
        self.tree_count = count        
        
    def setAngle(self, angle):
        self.image_angle = angle

    def setInter(self, inte):
        self.inter_spacing = inte

    def setPatterns(self, patterns_list):
        self.patterns = patterns_list
        
    def setCorner(self, CornerT):
        # min x, min y, max x, max y
        self.corner_tree_coords = CornerT

    def setRowNumbers(self, rownum):
        self.row_count = rownum

    def setTreesPerRow(self, TRcount):
        self.avg_tree_row = TRcount

    def setRoadCount(self, Rcount):
        road_count = Rcount
        
    """Outputs data to a file and the terminal"""
    def writeDataToFile(self, filename):
        print()
        print("The intra-row spacing mean value is: " + str(self.intra_spacing))
        print("The inter-row spacing mean value is: " + str(self.inter_spacing))
        print("The Tree count detected is: " + str(self.tree_count))
        print("The number of rows detected is: " + str(self.row_count))
        print("The mean value per row is: " + str(self.avg_tree_row))
        print("There were " + str(self.road_count) + ' road(s) or ditches detected')
        for point in self.corner_tree_coords:
            print("A corner coordinate is: " + str(point.x) + " , " + str(point.y))
        print("The detected pattern(s) are " + self.patterns)

        # Write to the outputFile
        with open(str(filename) + '.txt', 'w') as f:
            f.write("The intra-row spacing mean value is: " + str(self.intra_spacing) + '\n')
            f.write("The inter-row spacing mean value is: " + str(self.inter_spacing) + '\n')
            f.write("The Tree count detected is: " + str(self.tree_count) + '\n')
            f.write("The number of rows detected is: " + str(self.row_count) + '\n')
            f.write("The mean value per row is: " + str(self.avg_tree_row) + '\n')
            f.write("There were " + str(self.road_count) + ' road(s) or ditches detected\n')
            for point in self.corner_tree_coords:
                f.write("A corner coordinate is: " + str(point.x) + " , " + str(point.y) + '\n')
            f.write("The detected pattern(s) are " + self.patterns)

        print("Data written to " + str(filename) + ".txt")

        
        