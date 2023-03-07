#include "algorithms.hpp"
#include "classes.hpp"

#include <iostream>
#include <fstream>
#include <chrono>
#include <sys/resource.h>

int main(int argc, char** argv)
{  
    setlocale(LC_ALL,"ru_RU.UTF-8");  

    auto start_program = std::chrono::high_resolution_clock::now();
    struct rusage rusage;

    std::map<std::string, uint32_t> station_name_to_id;
    std::map<uint32_t, std::string> station_id_to_name;
    uint32_t next_station_id = 0;

    std::map<std::string, uint32_t> vehicle_name_to_id;
    std::map<uint32_t, std::string> vehicle_id_to_name;
    uint32_t next_vehicle_id = 0;

    CruisesGraph graph;

    std::ifstream in("input.txt");
    std::string line;
    if (in.is_open())
    {
        while (getline(in, line))
        {
            if (line[0] != '#')
            {
                line += ' ';
                std::string words[3];
                std::string nums[2];
                bool parsing_word = false;
                bool parsing_num = false;
                std::string current_word = "";
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
                std::string from = words[0];
                std::string to = words[1];
                std::string vehicle = words[2];
                std::string time_str = nums[0];
                std::string cost_str = nums[1];
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

                    Cruise new_cruise(station_name_to_id[from], station_name_to_id[to], vehicle_name_to_id[vehicle], cruise_time, cruise_cost);
                    graph.insertCruise(new_cruise);
                }
            }
        }
    }
    in.close();

    // for (auto pair : graph)
    // {
    //     std::cout << station_id_to_name[pair.first] << ": ";
    //     for (auto p : pair.second)
    //     {
    //         std::cout << station_id_to_name[p.first];
    //         std::vector<Cruise*> cruises = p.second;
    //         for (auto cruise : cruises)
    //         {
    //             std::cout << " (" << station_id_to_name[cruise->from_id] << " " << station_id_to_name[cruise->to_id] << " " << vehicle_id_to_name[cruise->vehicle_id] << " " << cruise->cruise_time << " " << cruise->cruise_cost << "), ";
    //         }
    //     }
    //     std::cout << std::endl;
    // }

    for (;;)
    {
        std::cout << "Введите тип запроса (1/2/3/4/5) или 'quit', если хотите выйти из программы> ";
        std::string task_type_str;
        getline(std::cin, task_type_str);
        if (task_type_str == "quit")
        {
            break;
        }
        uint32_t task_type = stoi(task_type_str);
        std::string vehicles_types_num_str;
        std::cout << "Введите число допустимых видов транспорта> ";
        getline(std::cin, vehicles_types_num_str);
        uint32_t vehicles_types_num = stoi(vehicles_types_num_str);
        std::unordered_set<uint32_t> vehicles_types;
        for (uint32_t i = 1; i <= vehicles_types_num; i++)
        {
            std::cout << "Введите допустимый вид транспорта #" << i << "> ";
            std::string vehicle_type;
            getline(std::cin, vehicle_type);
            vehicles_types.insert(vehicle_name_to_id[vehicle_type]);
        }
        switch (task_type)
        {
            case 1:
            {
                std::string station_from, station_to;
                std::cout << "Введите станцию отправления> ";
                getline(std::cin, station_from);
                std::cout << "Введите станцию прибытия> ";
                getline(std::cin, station_to);
                uint32_t from_id, to_id;
                from_id = station_name_to_id[station_from];
                to_id = station_name_to_id[station_to];

                auto start_operation = std::chrono::high_resolution_clock::now();
                std::tuple<std::vector<uint32_t>, std::vector<uint32_t>, std::vector<Cruise>> d_extra_p = dijkstra_extra_cond(from_id, next_station_id, graph, 0, vehicles_types);

                Trip trip;
                uint32_t current_station = to_id;
                while (current_station != from_id)
                {
                    Cruise next_cruise = std::get<2>(d_extra_p)[current_station];
                    trip += next_cruise;
                    current_station = next_cruise.from_id;
                }
                auto end_operation = std::chrono::high_resolution_clock::now();
                std::chrono::duration<double> operation_time = end_operation - start_operation;
                std::cout << "Время выполнения запроса: " << operation_time.count() << " сек." << std::endl;

                if (getrusage(RUSAGE_SELF, &rusage) != -1)
                    std::cout << "Max RSS: " << (double)rusage.ru_maxrss << " KiB" << std::endl;
                
                for (uint32_t count = 0; count < trip.cruises_num; count++)
                {
                    Cruise cruise = trip[count];
                    std::cout << (count + 1) << ") ";
                    std::cout << "Из: " << station_id_to_name[cruise.from_id] << ", в: " << station_id_to_name[cruise.to_id];
                    std::cout << ", Вид транспорта: " << vehicle_id_to_name[cruise.vehicle_id] << ", Время: " << cruise.cruise_time << ", Стоимость: " << cruise.cruise_cost << std::endl;
                }
                continue;
            }
            case 2:
            {
                std::string station_from, station_to;
                std::cout << "Введите станцию отправления> ";
                getline(std::cin, station_from);
                std::cout << "Введите станцию прибытия> ";
                getline(std::cin, station_to);
                uint32_t from_id, to_id;
                from_id = station_name_to_id[station_from];
                to_id = station_name_to_id[station_to];

                auto start_operation = std::chrono::high_resolution_clock::now();
                std::pair<std::vector<uint32_t>, std::vector<Cruise>> d_p = dijkstra(from_id, next_station_id, graph, 1, vehicles_types);

                Trip trip;
                uint32_t current_station = to_id;
                while (current_station != from_id)
                {
                    Cruise next_cruise = d_p.second[current_station];
                    trip += next_cruise;
                    current_station = next_cruise.from_id;
                }
                auto end_operation = std::chrono::high_resolution_clock::now();
                std::chrono::duration<double> operation_time = end_operation - start_operation;
                std::cout << "Время выполнения запроса: " << operation_time.count() << " сек." << std::endl;

                if (getrusage(RUSAGE_SELF, &rusage) != -1)
                    std::cout << "Max RSS: " << (double)rusage.ru_maxrss << " KiB" << std::endl;
                
                for (uint32_t count = 0; count < trip.cruises_num; count++)
                {
                    Cruise cruise = trip[count];
                    std::cout << (count + 1) << ") ";
                    std::cout << "Из: " << station_id_to_name[cruise.from_id] << ", в: " << station_id_to_name[cruise.to_id];
                    std::cout << ", Вид транспорта: " << vehicle_id_to_name[cruise.vehicle_id] << ", Время: " << cruise.cruise_time << ", Стоимость: " << cruise.cruise_cost << std::endl;
                }
                continue;
            }
            case 3:
            {
                std::string station_from, station_to;
                std::cout << "Введите станцию отправления> ";
                getline(std::cin, station_from);
                std::cout << "Введите станцию прибытия> ";
                getline(std::cin, station_to);
                uint32_t from_id, to_id;
                from_id = station_name_to_id[station_from];
                to_id = station_name_to_id[station_to];

                auto start_operation = std::chrono::high_resolution_clock::now();
                std::pair<std::vector<uint32_t>, std::vector<Cruise>> d_p = bfs(from_id, next_station_id, graph, vehicles_types);

                Trip trip;
                uint32_t current_station = to_id;
                while (current_station != from_id)
                {
                    Cruise next_cruise = d_p.second[current_station];
                    trip += next_cruise;
                    current_station = next_cruise.from_id;
                }
                auto end_operation = std::chrono::high_resolution_clock::now();
                std::chrono::duration<double> operation_time = end_operation - start_operation;
                std::cout << "Время выполнения запроса: " << operation_time.count() << " сек." << std::endl;

                if (getrusage(RUSAGE_SELF, &rusage) != -1)
                    std::cout << "Max RSS: " << (double)rusage.ru_maxrss << " KiB" << std::endl;
                
                for (uint32_t count = 0; count < trip.cruises_num; count++)
                {
                    Cruise cruise = trip[count];
                    std::cout << (count + 1) << ") ";
                    std::cout << "Из: " << station_id_to_name[cruise.from_id] << ", в: " << station_id_to_name[cruise.to_id];
                    std::cout << ", Вид транспорта: " << vehicle_id_to_name[cruise.vehicle_id] << ", Время: " << cruise.cruise_time << ", Стоимость: " << cruise.cruise_cost << std::endl;
                }
                continue;
            }
            case 4:
            {
                std::string station_from, limit_cost_str;
                std::cout << "Введите станцию отправления> ";
                getline(std::cin, station_from);
                std::cout << "Введите лимит стоимости> ";
                getline(std::cin, limit_cost_str);
                uint32_t from_id, limit_cost;
                from_id = station_name_to_id[station_from];
                limit_cost = stoi(limit_cost_str);

                auto start_operation = std::chrono::high_resolution_clock::now();
                std::pair<std::vector<uint32_t>, std::vector<Cruise>> d_p = dijkstra(from_id, next_station_id, graph, 1, vehicles_types);

                std::map<uint32_t, Trip> trips_map;
                for (uint32_t i = 0; i < next_station_id; i++)
                {
                    if (i != from_id && d_p.first[i] <= limit_cost)
                    {
                        Trip trip;
                        uint32_t current_station = i;
                        while (current_station != from_id)
                        {
                            Cruise next_cruise = d_p.second[current_station];
                            trip += next_cruise;
                            current_station = next_cruise.from_id;
                        }
                        trips_map[i] = trip;
                    }
                }
                auto end_operation = std::chrono::high_resolution_clock::now();
                std::chrono::duration<double> operation_time = end_operation - start_operation;
                std::cout << "Время выполнения запроса: " << operation_time.count() << " сек." << std::endl;

                if (getrusage(RUSAGE_SELF, &rusage) != -1)
                    std::cout << "Max RSS: " << (double)rusage.ru_maxrss << " KiB" << std::endl;

                for (auto station_from_and_trip : trips_map)
                {
                    std::string station_from = station_id_to_name[station_from_and_trip.first];
                    Trip trip = station_from_and_trip.second;

                    std::cout << "До станции '" << station_from << "':" << std::endl;

                    for (uint32_t count = 0; count < trip.cruises_num; count++)
                    {
                        Cruise cruise = trip[count];
                        std::cout << (count + 1) << ") ";
                        std::cout << "Из: " << station_id_to_name[cruise.from_id] << ", в: " << station_id_to_name[cruise.to_id];
                        std::cout << ", Вид транспорта: " << vehicle_id_to_name[cruise.vehicle_id] << ", Время: " << cruise.cruise_time << ", Стоимость: " << cruise.cruise_cost << std::endl;
                    }
                }
                continue;
            }
            case 5:
            {
                std::string station_from, limit_time_str;
                std::cout << "Введите станцию отправления> ";
                getline(std::cin, station_from);
                std::cout << "Введите лимит времени> ";
                getline(std::cin, limit_time_str);
                uint32_t from_id, limit_time;
                from_id = station_name_to_id[station_from];
                limit_time = stoi(limit_time_str);
                
                auto start_operation = std::chrono::high_resolution_clock::now();
                std::pair<std::vector<uint32_t>, std::vector<Cruise>> d_p = dijkstra(from_id, next_station_id, graph, 0, vehicles_types);

                std::map<uint32_t, Trip> trips_map;
                for (uint32_t i = 0; i < next_station_id; i++)
                {
                    if (i != from_id && d_p.first[i] <= limit_time)
                    {
                        Trip trip;
                        uint32_t current_station = i;
                        while (current_station != from_id)
                        {
                            Cruise next_cruise = d_p.second[current_station];
                            trip += next_cruise;
                            current_station = next_cruise.from_id;
                        }
                        trips_map[i] = trip;
                    }
                }
                auto end_operation = std::chrono::high_resolution_clock::now();
                std::chrono::duration<double> operation_time = end_operation - start_operation;
                std::cout << "Время выполнения запроса: " << operation_time.count() << " сек." << std::endl;

                if (getrusage(RUSAGE_SELF, &rusage) != -1)
                    std::cout << "Max RSS: " << (double)rusage.ru_maxrss << " KiB" << std::endl;

                for (auto station_from_and_trip : trips_map)
                {
                    std::string station_from = station_id_to_name[station_from_and_trip.first];
                    Trip trip = station_from_and_trip.second;

                    std::cout << "До станции '" << station_from << "':" << std::endl;

                    for (uint32_t count = 0; count < trip.cruises_num; count++)
                    {
                        Cruise cruise = trip[count];
                        std::cout << (count + 1) << ") ";
                        std::cout << "Из: " << station_id_to_name[cruise.from_id] << ", в: " << station_id_to_name[cruise.to_id];
                        std::cout << ", Вид транспорта: " << vehicle_id_to_name[cruise.vehicle_id] << ", Время: " << cruise.cruise_time << ", Стоимость: " << cruise.cruise_cost << std::endl;
                    }
                }
                continue;
            }
            default:
            {
                std::cout << "Неверный номер запроса. Введите 1/2/3/4/5 или 'quit'" << std::endl;
                continue;
            }
        }
    }
    std::cout << "До свидания!" << std::endl;

    auto end_program = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> program_duration = end_program - start_program;
    std::cout << "Время выполнения программы: " << program_duration.count() << " сек." << std::endl;

    if (getrusage(RUSAGE_SELF, &rusage) != -1)
        std::cout << "Max RSS: " << (double)rusage.ru_maxrss << " KiB" << std::endl;

    return 0;
}