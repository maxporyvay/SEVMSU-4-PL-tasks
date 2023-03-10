#include "algorithms.hpp"
#include "classes.hpp"

#include <iostream>
#include <fstream>
#include <chrono>
#include <algorithm>
#include <sys/resource.h>
#include <ncurses.h>

bool is_digits(const std::string &str)
{
    return std::all_of(str.begin(), str.end(), ::isdigit);
}

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

    // for (auto pair : graph.graph)
    // {
    //     std::cout << station_id_to_name[pair.first] << ": ";
    //     for (auto p : pair.second)
    //     {
    //         std::cout << station_id_to_name[p.first];
    //         std::vector<Cruise> cruises = p.second;
    //         for (auto cruise : cruises)
    //         {
    //             std::cout << " (" << station_id_to_name[cruise.from_id] << " " << station_id_to_name[cruise.to_id] << " ";
    //             std::cout << vehicle_id_to_name[cruise.vehicle_id] << " " << cruise.cruise_time << " " << cruise.cruise_cost << "), ";
    //         }
    //     }
    //     std::cout << std::endl;
    // }

    initscr();
    bool want_to_exit = false;

    while (!want_to_exit)
    {
        uint32_t current_item_index = 0;
        bool choice_made = false;
        noecho();

        while (!choice_made)
        {
            clear();
            curs_set(0);
            keypad(stdscr, true); 
            addstr("Выберите желаемый режим работы программы:\n\n");
            refresh();
            const char *choices[6] = {"Нахождение пути минимальной стоимости среди кратчайших путей между двумя городами",
                                    "Нахождение пути минимальной стоимости между двумя городами",
                                    "Нахождение пути между двумя городами с минимальным числом пересадок",
                                    "Нахождение городов, достижимых из города отправления не более чем за лимит денег, и путей к ним",
                                    "Нахождение городов, достижимых из города отправления не более чем за лимит времени, и путей к ним",
                                    "Выйти из программы"};
            
            for (uint32_t i = 0; i < 6; i++)
            {
                if (i == current_item_index)
                {
                    attron(A_STANDOUT);
                    printw("%s\n", choices[i]);
                    attroff(A_STANDOUT);
                }
                else
                {
                    printw("%s\n", choices[i]);
                }
                refresh();
            }

            switch (getch())
            {
                case KEY_UP:
                {
                    if (current_item_index > 0)
                    {
                        current_item_index--; 
                    }
                    else
                    {
                        current_item_index = 5;
                    }
                    break;
                }

                case KEY_DOWN:
                {
                    if (current_item_index < 5)
                    {
                        current_item_index++;
                    }
                    else
                    {
                        current_item_index = 0;
                    }
                    break;
                }
                    
                case (int)'\n':
                {
                    choice_made = true;
                    break;
                }

                default:
                {
                    break;
                }
            }
        }
        keypad(stdscr, false); 

        std::unordered_set<uint32_t> vehicles_types;

        if (current_item_index >= 0 && current_item_index <= 4)
        {
            clear();
            echo();
            char vehicles_types_num_strchar[100];
            addstr("Введите число допустимых видов транспорта:\n");
            refresh();
            curs_set(1);
            getstr(vehicles_types_num_strchar);
            std::string vehicles_types_num_str(vehicles_types_num_strchar);
            while (vehicles_types_num_str == "" || !is_digits(vehicles_types_num_str) || stoi(vehicles_types_num_str) <= 0)
            {
                clear();
                addstr("Ошибка ввода. Введите число подходящих видов транспорта:\n");
                refresh();
                curs_set(1);
                getstr(vehicles_types_num_strchar);
                vehicles_types_num_str = vehicles_types_num_strchar;
            }
            uint32_t vehicles_types_num = stoi(vehicles_types_num_str);
            
            for (uint32_t i = 1; i <= vehicles_types_num; i++)
            {
                clear();
                printw("Введите подходящий вид транспорта #%i:\n", i);
                refresh();
                char vehicle_type_char[100];
                curs_set(1);
                getstr(vehicle_type_char);
                std::string vehicle_type(vehicle_type_char);
                while (vehicle_name_to_id.find(vehicle_type) == vehicle_name_to_id.end())
                {
                    clear();
                    printw("Введен несуществующий вид транспорта. Введите подходящий вид транспорта #%i:\n", i);
                    refresh();
                    curs_set(1);
                    getstr(vehicle_type_char);
                    vehicle_type = vehicle_type_char;
                }
                vehicles_types.insert(vehicle_name_to_id[vehicle_type]);
            }
        }

        switch (current_item_index)
        {
            case 0:
            {
                clear();
                char station_from_char[100];
                addstr("Введите станцию отправления:\n");
                refresh();
                curs_set(1);
                getstr(station_from_char);
                std::string station_from(station_from_char);
                while (station_name_to_id.find(station_from) == station_name_to_id.end())
                {
                    clear();
                    addstr("Введена недопустимая станция отправления. Введите станцию отправления:\n");
                    refresh();
                    curs_set(1);
                    getstr(station_from_char);
                    station_from = station_from_char;
                }
                clear();
                char station_to_char[100];
                addstr("Введите станцию прибытия:\n");
                refresh();
                curs_set(1);
                getstr(station_to_char);
                std::string station_to(station_to_char);
                while (station_name_to_id.find(station_to) == station_name_to_id.end())
                {
                    clear();
                    addstr("Введена недопустимая станция прибытия. Введите станцию прибытия:\n");
                    refresh();
                    curs_set(1);
                    getstr(station_to_char);
                    station_to = station_to_char;
                }
                uint32_t from_id, to_id;
                from_id = station_name_to_id[station_from];
                to_id = station_name_to_id[station_to];

                auto start_operation = std::chrono::high_resolution_clock::now();
                
                std::vector<uint32_t> d(next_station_id, INF);
                std::vector<uint32_t> extra(next_station_id, INF);
                std::vector<Cruise> p(next_station_id);
                dijkstra_extra_cond(from_id, graph, 0, vehicles_types, d, extra, p);

                Trip trip;
                uint32_t current_station = to_id;
                if (d[to_id] < INF)
                {
                    while (current_station != from_id)
                    {
                        Cruise next_cruise = p[current_station];
                        trip += next_cruise;
                        current_station = next_cruise.from_id;
                    }
                }
                auto end_operation = std::chrono::high_resolution_clock::now();
                std::chrono::duration<double> operation_time = end_operation - start_operation;
                printw("Время выполнения запроса: %f сек.\n", operation_time);
                refresh();

                if (getrusage(RUSAGE_SELF, &rusage) != -1)
                {
                    printw("Max RSS: %f KiB\n\n", (double)rusage.ru_maxrss);
                    refresh();
                }
                
                if (trip.cruises_num > 0)
                {
                    for (uint32_t count = 1; count <= trip.cruises_num; count++)
                    {
                        Cruise cruise = trip[count - 1];
                        std::string from = station_id_to_name[cruise.from_id];
                        std::string to = station_id_to_name[cruise.to_id];
                        std::string vehicle = vehicle_id_to_name[cruise.vehicle_id];
                        uint32_t time = cruise.cruise_time;
                        uint32_t cost = cruise.cruise_cost;
                        printw("%i) Из: %s, в: %s, транспорт: %s, время: %i, стоимость: %i\n", count, from.c_str(), to.c_str(), vehicle.c_str(), time, cost);
                        refresh();
                    }
                }
                else
                {
                    addstr("С помощью данных видов транспорта город прибытия не достижим из города отправления\n");
                    refresh();
                }
                addstr("Нажмите любую клавишу для перехода в меню\n");
                refresh();
                curs_set(0);
                getch();
                break;
            }

            case 1:
            {
                clear();
                char station_from_char[100];
                addstr("Введите станцию отправления:\n");
                refresh();
                curs_set(1);
                getstr(station_from_char);
                std::string station_from(station_from_char);
                while (station_name_to_id.find(station_from) == station_name_to_id.end())
                {
                    clear();
                    addstr("Введена недопустимая станция отправления. Введите станцию отправления:\n");
                    refresh();
                    curs_set(1);
                    getstr(station_from_char);
                    station_from = station_from_char;
                }
                clear();
                char station_to_char[100];
                addstr("Введите станцию прибытия:\n");
                refresh();
                curs_set(1);
                getstr(station_to_char);
                std::string station_to(station_to_char);
                while (station_name_to_id.find(station_to) == station_name_to_id.end())
                {
                    clear();
                    addstr("Введена недопустимая станция прибытия. Введите станцию прибытия:\n");
                    refresh();
                    curs_set(1);
                    getstr(station_to_char);
                    station_to = station_to_char;
                }
                uint32_t from_id, to_id;
                from_id = station_name_to_id[station_from];
                to_id = station_name_to_id[station_to];

                auto start_operation = std::chrono::high_resolution_clock::now();
                
                std::vector<uint32_t> d(next_station_id, INF);
                std::vector<Cruise> p(next_station_id);
                dijkstra(from_id, graph, 1, vehicles_types, d, p);

                Trip trip;
                uint32_t current_station = to_id;
                if (d[to_id] < INF)
                {
                    while (current_station != from_id)
                    {
                        Cruise next_cruise = p[current_station];
                        trip += next_cruise;
                        current_station = next_cruise.from_id;
                    }
                }
                auto end_operation = std::chrono::high_resolution_clock::now();
                std::chrono::duration<double> operation_time = end_operation - start_operation;
                printw("Время выполнения запроса: %f сек.\n", operation_time);
                refresh();

                if (getrusage(RUSAGE_SELF, &rusage) != -1)
                {
                    printw("Max RSS: %f KiB\n\n", (double)rusage.ru_maxrss);
                    refresh();
                }
                
                if (trip.cruises_num > 0)
                {
                    for (uint32_t count = 1; count <= trip.cruises_num; count++)
                    {
                        Cruise cruise = trip[count - 1];
                        std::string from = station_id_to_name[cruise.from_id];
                        std::string to = station_id_to_name[cruise.to_id];
                        std::string vehicle = vehicle_id_to_name[cruise.vehicle_id];
                        uint32_t time = cruise.cruise_time;
                        uint32_t cost = cruise.cruise_cost;
                        printw("%i) Из: %s, в: %s, транспорт: %s, время: %i, стоимость: %i\n", count, from.c_str(), to.c_str(), vehicle.c_str(), time, cost);
                        refresh();
                    }
                }
                else
                {
                    addstr("С помощью данных видов транспорта город прибытия не достижим из города отправления\n");
                    refresh();
                }
                addstr("Нажмите любую клавишу для перехода в меню\n");
                refresh();
                curs_set(0);
                getch();
                break;
            }

            case 2:
            {
                clear();
                char station_from_char[100];
                addstr("Введите станцию отправления:\n");
                refresh();
                curs_set(1);
                getstr(station_from_char);
                std::string station_from(station_from_char);
                while (station_name_to_id.find(station_from) == station_name_to_id.end())
                {
                    clear();
                    addstr("Введена недопустимая станция отправления. Введите станцию отправления:\n");
                    refresh();
                    curs_set(1);
                    getstr(station_from_char);
                    station_from = station_from_char;
                }
                clear();
                char station_to_char[100];
                addstr("Введите станцию прибытия:\n");
                refresh();
                curs_set(1);
                getstr(station_to_char);
                std::string station_to(station_to_char);
                while (station_name_to_id.find(station_to) == station_name_to_id.end())
                {
                    clear();
                    addstr("Введена недопустимая станция прибытия. Введите станцию прибытия:\n");
                    refresh();
                    curs_set(1);
                    getstr(station_to_char);
                    station_to = station_to_char;
                }
                uint32_t from_id, to_id;
                from_id = station_name_to_id[station_from];
                to_id = station_name_to_id[station_to];

                auto start_operation = std::chrono::high_resolution_clock::now();
                
                std::vector<uint32_t> d(next_station_id, INF);
                std::vector<uint32_t> extra(next_station_id, INF);
                std::vector<Cruise> p(next_station_id);
                bfs(from_id, graph, vehicles_types, d, p);

                Trip trip;
                uint32_t current_station = to_id;
                if (d[to_id] < INF)
                {
                    while (current_station != from_id)
                    {
                        Cruise next_cruise = p[current_station];
                        trip += next_cruise;
                        current_station = next_cruise.from_id;
                    }
                }
                auto end_operation = std::chrono::high_resolution_clock::now();
                std::chrono::duration<double> operation_time = end_operation - start_operation;
                printw("Время выполнения запроса: %f сек.\n", operation_time);
                refresh();

                if (getrusage(RUSAGE_SELF, &rusage) != -1)
                {
                    printw("Max RSS: %f KiB\n\n", (double)rusage.ru_maxrss);
                    refresh();
                }
                
                if (trip.cruises_num > 0)
                {
                    for (uint32_t count = 1; count <= trip.cruises_num; count++)
                    {
                        Cruise cruise = trip[count - 1];
                        std::string from = station_id_to_name[cruise.from_id];
                        std::string to = station_id_to_name[cruise.to_id];
                        std::string vehicle = vehicle_id_to_name[cruise.vehicle_id];
                        uint32_t time = cruise.cruise_time;
                        uint32_t cost = cruise.cruise_cost;
                        printw("%i) Из: %s, в: %s, транспорт: %s, время: %i, стоимость: %i\n", count, from.c_str(), to.c_str(), vehicle.c_str(), time, cost);
                        refresh();
                    }
                }
                else
                {
                    addstr("С помощью данных видов транспорта город прибытия не достижим из города отправления\n");
                    refresh();
                }
                addstr("Нажмите любую клавишу для перехода в меню\n");
                refresh();
                curs_set(0);
                getch();
                break;
            }

            case 3:
            {
                clear();
                char station_from_char[100];
                addstr("Введите станцию отправления:\n");
                refresh();
                curs_set(1);
                getstr(station_from_char);
                std::string station_from(station_from_char);
                while (station_name_to_id.find(station_from) == station_name_to_id.end())
                {
                    clear();
                    addstr("Введена недопустимая станция отправления. Введите станцию отправления:\n");
                    refresh();
                    curs_set(1);
                    getstr(station_from_char);
                    station_from = station_from_char;
                }
                clear();
                char limit_cost_char[100];
                addstr("Введите лимит стоимости:\n");
                refresh();
                curs_set(1);
                getstr(limit_cost_char);
                std::string limit_cost_str(limit_cost_char);               
                while (limit_cost_str == "" || !is_digits(limit_cost_str) || stoi(limit_cost_str) <= 0)
                {
                    clear();
                    addstr("Введена недопустимый лимит стоимости. Введите лимит стоимости:\n");
                    refresh();
                    curs_set(1);
                    getstr(limit_cost_char);
                    limit_cost_str = limit_cost_char;
                }
                uint32_t from_id, limit_cost;
                limit_cost = stoi(limit_cost_str);
                from_id = station_name_to_id[station_from];

                auto start_operation = std::chrono::high_resolution_clock::now();

                std::vector<uint32_t> d(next_station_id, INF);
                std::vector<Cruise> p(next_station_id);
                dijkstra(from_id, graph, 1, vehicles_types, d, p);

                std::map<uint32_t, Trip> trips_map;
                for (uint32_t i = 0; i < next_station_id; i++)
                {
                    if (i != from_id && d[i] <= limit_cost)
                    {
                        Trip trip;
                        uint32_t current_station = i;
                        while (current_station != from_id)
                        {
                            Cruise next_cruise = p[current_station];
                            trip += next_cruise;
                            current_station = next_cruise.from_id;
                        }
                        trips_map[i] = trip;
                    }
                }
                auto end_operation = std::chrono::high_resolution_clock::now();
                std::chrono::duration<double> operation_time = end_operation - start_operation;
                printw("Время выполнения запроса: %f сек.\n", operation_time);
                refresh();

                if (getrusage(RUSAGE_SELF, &rusage) != -1)
                {
                    printw("Max RSS: %f KiB\n\n", (double)rusage.ru_maxrss);
                    refresh();
                }

                if (!trips_map.empty())
                {
                    for (auto station_from_and_trip : trips_map)
                    {
                        std::string station_from = station_id_to_name[station_from_and_trip.first];
                        Trip trip = station_from_and_trip.second;

                        printw("До станции '%s':\n", station_from.c_str());
                        refresh();

                        for (uint32_t count = 1; count <= trip.cruises_num; count++)
                        {
                            Cruise cruise = trip[count - 1];
                            std::string from = station_id_to_name[cruise.from_id];
                            std::string to = station_id_to_name[cruise.to_id];
                            std::string vehicle = vehicle_id_to_name[cruise.vehicle_id];
                            uint32_t time = cruise.cruise_time;
                            uint32_t cost = cruise.cruise_cost;
                            printw("%i) Из: %s, в: %s, транспорт: %s, время: %i, стоимость: %i\n", count, from.c_str(), to.c_str(), vehicle.c_str(), time, cost);
                            refresh();
                        }
                    }
                }
                else
                {
                    addstr("С помощью данных видов транспорта ни один из городов не достижим из города отправления за данный лимит стоимости\n");
                    refresh();
                }
                addstr("Нажмите любую клавишу для перехода в меню\n");
                refresh();
                curs_set(0);
                getch();
                break;
            }

            case 4:
            {
                clear();
                char station_from_char[100];
                addstr("Введите станцию отправления:\n");
                refresh();
                curs_set(1);
                getstr(station_from_char);
                std::string station_from(station_from_char);
                while (station_name_to_id.find(station_from) == station_name_to_id.end())
                {
                    clear();
                    addstr("Введена недопустимая станция отправления. Введите станцию отправления:\n");
                    refresh();
                    curs_set(1);
                    getstr(station_from_char);
                    station_from = station_from_char;
                }
                clear();
                char limit_time_char[100];
                addstr("Введите лимит времени:\n");
                refresh();
                curs_set(1);
                getstr(limit_time_char);
                std::string limit_time_str(limit_time_char);               
                while (limit_time_str == "" || !is_digits(limit_time_str) || stoi(limit_time_str) <= 0)
                {
                    clear();
                    addstr("Введена недопустимый лимит времени. Введите лимит времени:\n");
                    refresh();
                    curs_set(1);
                    getstr(limit_time_char);
                    limit_time_str = limit_time_char;
                }
                uint32_t from_id, limit_time;
                limit_time = stoi(limit_time_str);
                from_id = station_name_to_id[station_from];

                auto start_operation = std::chrono::high_resolution_clock::now();

                std::vector<uint32_t> d(next_station_id, INF);
                std::vector<Cruise> p(next_station_id);
                dijkstra(from_id, graph, 0, vehicles_types, d, p);

                std::map<uint32_t, Trip> trips_map;
                for (uint32_t i = 0; i < next_station_id; i++)
                {
                    if (i != from_id && d[i] <= limit_time)
                    {
                        Trip trip;
                        uint32_t current_station = i;
                        while (current_station != from_id)
                        {
                            Cruise next_cruise = p[current_station];
                            trip += next_cruise;
                            current_station = next_cruise.from_id;
                        }
                        trips_map[i] = trip;
                    }
                }
                auto end_operation = std::chrono::high_resolution_clock::now();
                std::chrono::duration<double> operation_time = end_operation - start_operation;
                printw("Время выполнения запроса: %f сек.\n", operation_time);
                refresh();

                if (getrusage(RUSAGE_SELF, &rusage) != -1)
                {
                    printw("Max RSS: %f KiB\n\n", (double)rusage.ru_maxrss);
                    refresh();
                }

                if (!trips_map.empty())
                {
                    for (auto station_from_and_trip : trips_map)
                    {
                        std::string station_from = station_id_to_name[station_from_and_trip.first];
                        Trip trip = station_from_and_trip.second;

                        printw("До станции '%s':\n", station_from.c_str());
                        refresh();

                        for (uint32_t count = 1; count <= trip.cruises_num; count++)
                        {
                            Cruise cruise = trip[count - 1];
                            std::string from = station_id_to_name[cruise.from_id];
                            std::string to = station_id_to_name[cruise.to_id];
                            std::string vehicle = vehicle_id_to_name[cruise.vehicle_id];
                            uint32_t time = cruise.cruise_time;
                            uint32_t cost = cruise.cruise_cost;
                            printw("%i) Из: %s, в: %s, транспорт: %s, время: %i, стоимость: %i\n", count, from.c_str(), to.c_str(), vehicle.c_str(), time, cost);
                            refresh();
                        }
                    }
                }
                else
                {
                    addstr("С помощью данных видов транспорта ни один из городов не достижим из города отправления за данный лимит времени\n");
                    refresh();
                }
                addstr("Нажмите любую клавишу для перехода в меню\n");
                refresh();
                curs_set(0);
                getch();
                break;
            }

            case 5:
            {
                want_to_exit = true;
                break;
            }

            default:
            {
                break;
            }
        }
    }

    endwin();

    auto end_program = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> program_duration = end_program - start_program;
    std::cout << "Время выполнения программы: " << program_duration.count() << " сек." << std::endl;

    if (getrusage(RUSAGE_SELF, &rusage) != -1)
    {
        std::cout << "Max RSS: " << (double)rusage.ru_maxrss << " KiB" << std::endl;
    }

    return 0;
}