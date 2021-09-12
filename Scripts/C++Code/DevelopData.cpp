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
	int offset = 1;
	for (int y = 0; y < 100; y++){		
		for (int x = 0; x < 100; x++){
			toReturn[count][0] = x * 10 ;
			toReturn[count][1] = y * 10 ;
			count += 1;
			
			// if(y % 2 == 0){
			// 	toReturn[count][0] += offset;
			// } 
		}
	}
	// Quincunx Center point
	for (int y = 0; y < 99; y++){
		for (int x = 0; x < 99; x++){
			toReturn[count][0] = x * 10 + 5;
			toReturn[count][1] = y * 10 + 55;
			count++;
		}
	}
	//write code to output to a file
	ofstream MyFile;
	MyFile.open("QuincunxIdeal.txt");
	for (int x = 0; x < count; x++){
		MyFile << toReturn[x][0] << " " << toReturn[x][1] << endl;
	}
	MyFile.close();
	}
	// 		count++;
	// 	}
	// 	if(y%2 ==0){
	// 			offset +=1;
	// 		} else {
	// 			offset+=3;
	// 		}
	// }
	// Quincunx Center point
	// for (int y = 0; y < 9; y++){
	// 	for (int x = 0; x < 9; x++){
	// 		toReturn[count][0] = x * 3 + 1.5;
	// 		toReturn[count][1] = y * 3 + 1.5;
			// if(y % 2 == 0){
			// 	toReturn[count][0] += offset;
			// } 
	// 		count++;
	// 	}
	// }