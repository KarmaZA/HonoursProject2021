// This is a program to develop test data
// Small program no use of .h file

#include <iostream>
#include <fstream>
#include <stdio.h>
#include <stdlib.h>

using namespace std;		

int main(){
	int count = 0;
	double toReturn[19801][2];
	int offset = 5; 
	int cord = 0;
	for (int y = 0; y < 100; y++){		
		cord = 0;
		for (int x = 0; x < 100; x++){	
			toReturn[count][0] = cord;
			toReturn[count][1] = y * 10 ;
			count += 1;		
			if(x % 2 == 0){
				 cord += 4;
			} else {
				cord += 8;
			}
		}
	}
	//write code to output to a file
	ofstream MyFile;
	MyFile.open("DoubleRowIdeal.txt");
	for (int x = 0; x < count; x++){
		MyFile << toReturn[x][0] << " " << toReturn[x][1] << endl;
	}
	MyFile.close();
	}