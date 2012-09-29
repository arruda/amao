#include <iostream>
using namespace std;

int main(void)
{
   int *i = new int[2];
   for(int ii=0;ii<100000;ii++){
        i[ii]=ii;
    }
   i[123456789987654321]=5;
   cout << i[100000];
   cout << "Hello World!" << endl;
   return 0;
}
