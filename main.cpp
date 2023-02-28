#include "algorithms.h"
#include "classes.h"

#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <utility>
#include <vector>
#include <queue>
#include <unordered_set>
#include <stdint.h>

using namespace std;

map<string, uint32_t> station_name_to_id;
map<uint32_t, string> station_id_to_name;
uint32_t next_station_id = 0;

map<string, uint32_t> vehicle_name_to_id;
map<uint32_t, string> vehicle_id_to_name;
uint32_t next_vehicle_id = 0;

map<uint32_t, map<uint32_t, vector<Cruise*>>> graph;

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
                uint32_t word_count = 0;
                uint32_t num_count = 0;
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
                    uint32_t cruise_time = stoi(time_str);
                    uint32_t cruise_cost = stoi(cost_str);

                    if (station_name_to_id.find(from) == station_name_to_id.end())
                    {
                        station_name_to_id[from] = next_station_id;
                        station_id_to_name[next_station_id] = from;
                        next_station_id++;
                    }
                    if (station_name_to_id.find(to) == station_name_to_id.end())
                    {
                        station_name_to_id[to] = next_station_id;
                        station_id_to_name[next_station_id] = to;
                        next_station_id++;
                    }
                    if (vehicle_name_to_id.find(vehicle) == vehicle_name_to_id.end())
                    {
                        vehicle_name_to_id[vehicle] = next_vehicle_id;
                        vehicle_id_to_name[next_vehicle_id] = vehicle;
                        next_vehicle_id++;
                    }

                    Cruise *new_cruise = new Cruise(station_name_to_id[from], station_name_to_id[to], vehicle_name_to_id[vehicle], cruise_time, cruise_cost);

                    if (graph.find(station_name_to_id[from]) == graph.end())
                    {
                        map<uint32_t, vector<Cruise*>> in_map;
                        vector<Cruise*> in_vec;
                        in_vec.push_back(new_cruise);
                        in_map[station_name_to_id[to]] = in_vec;
                        graph[station_name_to_id[from]] = in_map;
                    }
                    else if (graph[station_name_to_id[from]].find(station_name_to_id[to]) == graph[station_name_to_id[from]].end())
                    {
                        vector<Cruise*> in_vec;
                        in_vec.push_back(new_cruise);
                        graph[station_name_to_id[from]][station_name_to_id[to]] = in_vec;
                    }
                    else
                    {
                        graph[station_name_to_id[from]][station_name_to_id[to]].push_back(new_cruise);
                    }    
                }
            }
        }
    }
    in.close();

    // for (auto pair : graph)
    // {
    //     cout << station_id_to_name[pair.first] << ": ";
    //     for (auto p : pair.second)
    //     {
    //         cout << station_id_to_name[p.first];
    //         vector<Cruise*> cruises = p.second;
    //         for (auto cruise : cruises)
    //         {
    //             cout << " (" << station_id_to_name[cruise->from_id] << " " << station_id_to_name[cruise->to_id] << " " << vehicle_id_to_name[cruise->vehicle_id] << " " << cruise->cruise_time << " " << cruise->cruise_cost << "), ";
    //         }
    //     }
    //     cout << endl;
    // }

    for (;;)
    {
        cout << "Enter task type (1/2/3/4/5) or 'quit' if you want to quit> ";
        string task_type_str;
        cin >> task_type_str;
        if (task_type_str == "quit")
        {
            break;
        }
        uint32_t task_type = stoi(task_type_str);
        string vehicles_types_num_str;
        cout << "Enter wanted vehicles types number> ";
        cin >> vehicles_types_num_str;
        uint32_t vehicles_types_num = stoi(vehicles_types_num_str);
        cout << "Enter wanted vehicles types splitted by spaces> ";
        unordered_set<uint32_t> vehicles_types;
        for (uint32_t i = 0; i < vehicles_types_num; i++)
        {
            string vehicle_type;
            cin >> vehicle_type;
            vehicles_types.insert(vehicle_name_to_id[vehicle_type]);
        }
        switch (task_type)
        {
            case 1:
            {
                string station_from, station_to;
                cout << "Enter station_from and station_to splitted by space> ";
                cin >> station_from >> station_to;
                uint32_t from_id, to_id;
                from_id = station_name_to_id[station_from];
                to_id = station_name_to_id[station_to];
                continue;
            }
            case 2:
            {
                string station_from, station_to;
                cout << "Enter station_from and station_to splitted by space> ";
                cin >> station_from >> station_to;
                uint32_t from_id, to_id;
                from_id = station_name_to_id[station_from];
                to_id = station_name_to_id[station_to];
                pair<vector<uint32_t>, vector<uint32_t>> d_p = dijkstra(from_id, next_station_id, graph, 1, vehicles_types);

                // for (auto v : vehicles_types)
                //     cout << v << " ";
                // cout << endl;

                // for (auto p : vehicle_id_to_name)
                //     cout << p.first << ": " << p.second << ", ";
                // cout << endl;

                // for (uint32_t i = 0; i < d_p.first.size(); i++)
                // {
                //     cout << d_p.first[i] << " ";
                // }
                // cout << endl;
                // for (uint32_t i = 0; i < d_p.second.size(); i++)
                // {
                //     cout << d_p.second[i] << " ";
                // }
                // cout << endl;

                uint32_t current_station = to_id;
                while (current_station != from_id)
                {
                    cout << station_id_to_name[current_station] << " ";
                    current_station = d_p.second[current_station];
                }
                cout << station_id_to_name[from_id] << endl;
                continue;
            }
            case 3:
            {
                string station_from, station_to;
                cout << "Enter station_from and station_to splitted by space> ";
                cin >> station_from >> station_to;
                uint32_t from_id, to_id;
                from_id = station_name_to_id[station_from];
                to_id = station_name_to_id[station_to];
                continue;
            }
            case 4:
            {
                string station_from, limit_cost_str;
                cout << "Enter station_from and limit_cost splitted by space> ";
                cin >> station_from >> limit_cost_str;
                uint32_t from_id, limit_cost;
                from_id = station_name_to_id[station_from];
                limit_cost = stoi(limit_cost_str);
                pair<vector<uint32_t>, vector<uint32_t>> d_p = dijkstra(from_id, next_station_id, graph, 1, vehicles_types);

                for (uint32_t i = 0; i < next_station_id; i++)
                {
                    if (i != from_id && d_p.first[i] <= limit_cost)
                    {
                        uint32_t current_station = i;
                        while (current_station != from_id)
                        {
                            cout << station_id_to_name[current_station] << " ";
                            current_station = d_p.second[current_station];
                        }
                        cout << station_id_to_name[from_id] << endl;
                    }
                }
                continue;
            }
            case 5:
            {
                string station_from, limit_time_str;
                cout << "Enter station_from and limit_time splitted by space> ";
                cin >> station_from >> limit_time_str;
                uint32_t from_id, limit_time;
                from_id = station_name_to_id[station_from];
                limit_time = stoi(limit_time_str);
                pair<vector<uint32_t>, vector<uint32_t>> d_p = dijkstra(from_id, next_station_id, graph, 0, vehicles_types);

                for (uint32_t i = 0; i < next_station_id; i++)
                {
                    if (i != from_id && d_p.first[i] <= limit_time)
                    {
                        uint32_t current_station = i;
                        while (current_station != from_id)
                        {
                            cout << station_id_to_name[current_station] << " ";
                            current_station = d_p.second[current_station];
                        }
                        cout << station_id_to_name[from_id] << endl;
                    }
                }
                continue;
            }
            default:
            {
                cout << "Not valid task type" << endl;
                continue;
            }
        }
    }
    cout << "Good Bye!" << endl;

    return 0;
}