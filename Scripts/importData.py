# File for importing the Data from files
# Also will be used for creating and manipulating data structures
from logging import error
import geopandas as gpd

# Using Geopandas as it is updated more frequently
def importGeoJSONData(filename):
    try:
        with open(filename) as f:
        #data is a pandas.dataframe variable type
            data = gpd.read_file(f)
      
        # Note use of iterrows() to iterate   
        # for element, row in data.iterrows():
        #    print(element, row)
        #print(data)
        return data
    except:
        print("File not found")
        return error