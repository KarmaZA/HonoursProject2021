// This is a program to develop test data
// Small program no use of .h file

#include <iostream>
#include <fstream>
#include <stdio.h>
#include <stdlib.h>


using namespace std;

			

int main(){
	int count = 0;
	double toReturn[181][2];
	int offset = 1;
	for (int y = 0; y < 10; y++){		
		for (int x = 0; x < 10; x++){
			toReturn[count][0] = x * 1;
			toReturn[count][1] = offset;
			// if(y % 2 == 0){
			// 	toReturn[count][0] += offset;
			// } 
			count++;
		}
		if(y%2 ==0){
				offset +=1;
			} else {
				offset+=3;
			}
	}

	// for (int y = 0; y < 9; y++){
	// 	for (int x = 0; x < 9; x++){
	// 		toReturn[count][0] = x * 3 + 1.5;
	// 		toReturn[count][1] = y * 3 + 1.5;
	// 		// if(y % 2 == 0){
	// 		// 	toReturn[count][0] += offset;
	// 		// } 
	// 		count++;
	// 	}
	// }
	//Noise
	// for (int x = 0; x < 100; x++){
	// 	//Randomise the data
	// 	int add_noise = rand() % 6;
	// 	if (add_noise == 0){
	// 		double noise = 0.5 - ((rand()%10)/10.00);
	// 		cout << noise << endl;
	// 		if((rand()%2) == 0){
	// 			toReturn[x][0] += noise;
	// 		} else {
	// 			toReturn[x][1] += noise;
	// 		}
			
	// 	}
	// }
	//write code to output to a file
	ofstream MyFile;
	MyFile.open("DoubleHedgeIdeal3.txt");
	for (int x = 0; x < count; x++){
		MyFile << toReturn[x][0] << " " << toReturn[x][1] << endl;
	}
	MyFile.close();
}