# HonoursProject2021
This is my Honours project that will make use of image matching to determine planting patterns in images of crops and extract data about their parameters.

This is a project for the company Aerobotics and will use Python to develop this application.

To run this program you need the requisite python libraries installed: matplotlib, numpy, shapely, imutils, imageio and sklearn

Data must be stored in the correct folder for the program to find it. GeoJSON files in the Data/ReadWorldData and idealized data in .txt files in Data/IdealData.

To run the program use the bash script run.sh and the input the file name when prompted. And any file paths if in a sub-folder of the correct data location.

If the cleanup does not work correctly for some reason you can run the clean.sh script to delete all template and sub-images.

Output is stored in 'filename'.txt for the parameters and detected pattern. The scoring for the patterns is stored in TM'filename'