# File for importing the Data from files
# Also will be used for creating and manipulating data structures
import json

# 
def importGeoJSONData(filename):
    with open(filename) as f:
        data = json.loads(f.read())
    return data