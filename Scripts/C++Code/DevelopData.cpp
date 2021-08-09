// This is a program to develop test data
// Small program no use of .h file

#include <iostream>
#include <fstream>

using namespace std;
			

int main(){
	int count = 0;
	int toReturn[100][2];
	for (int x = 0; x < 10; x++){
		for (int y = 0; y < 10; y++){
			toReturn[count][0] = x * 3;
			toReturn[count][1] = y * 3;
			count++;
		}
	}
	//write code to output to a file
	ofstream MyFile;
	MyFile.open("SquareIdeal3.txt");
	for (int x = 0; x < count; x++){
		MyFile << toReturn[x][0] << " " << toReturn[x][1] << endl;
	}

	MyFile.close();
}
