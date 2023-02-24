#include "algorithms.h"
#include "classes.h"

#include <iostream>
#include <fstream>
#include <string>
#include <map>

using namespace std;

map<string, int> station_name_to_id;
map<int, string> station_id_to_name;
int max_station_id = -1;

map<string, int> vehicle_name_to_id;
map<int, string> vehicle_id_to_name;
int max_vehicle_id = -1;

int main(int argc, char** argv)
{  
    ifstream in("input.txt");
    string line;
    if (in.is_open())
    {
        while (getline(in, line))
        {
            if (line[0] != '#')
            {
                line += ' ';
                string words[3];
                string nums[2];
                bool parsing_word = false;
                bool parsing_num = false;
                string current_word = "";
                int word_count = 0;
                int num_count = 0;
                for (char sym : line)
                {
                    if (parsing_word)
                    {
                        if (sym == '"')
                        {
                            parsing_word = false;
                            words[word_count] = current_word;
                            current_word = "";
                            word_count++;
                        }
                        else
                        {
                            current_word += sym;
                        }
                    }
                    else if (sym == '"')
                    {
                        parsing_word = true;
                    }
                    else if (sym == ' ')
                    {
                        if (num_count < 2)
                        {
                            if (parsing_num)
                            {
                                nums[num_count] = current_word;
                                current_word = "";
                                parsing_num = false;
                                num_count++;
                            }
                        }
                        else
                        {
                            break;
                        }
                    }
                    else
                    {
                        parsing_num = true;
                        current_word += sym;
                    }
                }
                string from = words[0];
                string to = words[1];
                string vehicle = words[2];
                string time_str = nums[0];
                string cost_str = nums[1];
                if (from != "")
                {
                    int time = stoi(time_str);
                    int cost = stoi(cost_str);

                    if (station_name_to_id.find(from) == station_name_to_id.end())
                    {
                        max_station_id++;
                        station_name_to_id[from] = max_station_id;
                        station_id_to_name[max_station_id] = from;
                    }
                    if (station_name_to_id.find(to) == station_name_to_id.end())
                    {
                        max_station_id++;
                        station_name_to_id[to] = max_station_id;
                        station_id_to_name[max_station_id] = to;
                    }
                    if (vehicle_name_to_id.find(vehicle) == vehicle_name_to_id.end())
                    {
                        max_vehicle_id++;
                        vehicle_name_to_id[vehicle] = max_vehicle_id;
                        vehicle_id_to_name[max_vehicle_id] = vehicle;
                    }

                    Cruise *new_cruise = new Cruise(station_name_to_id[from], station_name_to_id[to], vehicle_name_to_id[vehicle], time, cost);       
                }
            }
        }
    }
    in.close(); 

    return 0;
}