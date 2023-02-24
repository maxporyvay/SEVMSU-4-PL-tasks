#include "algorithms.h"
#include "classes.h"

#include <iostream>
#include <fstream>
#include <map>

using namespace std;

int main(int argc, char** argv)
{
    // cout << sizeof(int) << endl;
    ifstream in("input.txt");
    if (in.is_open())
    {
        while (getline(in, line))
        {
            cout << line << endl;
        }
    }
    in.close(); 

    return 0;
}