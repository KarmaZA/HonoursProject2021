# /bin/bash

g++ -c DevelopData.cpp
g++ -o runDevelopData DevelopData.o
./runDevelopData

rm DevelopData.o runDevelopData
