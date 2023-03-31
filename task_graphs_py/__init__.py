from task_graphs_py.classes import INF, Cruise, Trip, CruisesGraph
from task_graphs_py.algorithms import bfs, dijkstra, dijkstra_extra_cond

import curses
import sys

# #include <sys/resource.h>


OPTIONS_NUM = 6

MINCOST_MINTIME_MODE = 0
MINCOST_MODE = 1
MINSTATIONSNUM_MODE = 2
LIMITCOST_MODE = 3
LIMITTIME_MODE = 4
WANT_TO_EXIT = 5


def main():
    # setlocale(LC_ALL,"ru_RU.UTF-8");  

    # auto start_program = std::chrono::high_resolution_clock::now();
    # struct rusage rusage;

    station_name_to_id = {}
    station_id_to_name = {}
    next_station_id = 0

    vehicle_name_to_id = {}
    vehicle_id_to_name = {}
    next_vehicle_id = 0

    graph = CruisesGraph()

    filename = 'input.txt'
    if (len(sys.argv) == 2):
        filename = sys.argv[1]

    want_to_exit = False
    # std::ofstream log("log.txt", std::ios_base::app)
    
    # std::time_t timestamp = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now())
    # log << std::ctime(&timestamp) << std::endl

    try:
        with open(filename, 'r', encoding='UTF-8') as f:
            for line in f:
                line = line.strip().split('#')[0]
                if line:
                    _, from_st, _, to_st, _, vehicle, other = line.split('"')
                    time_str, cost_str = other.split()
                    time_ = int(time_str)
                    cost_ = int(cost_str)

                    if from_st not in station_name_to_id:
                        station_name_to_id[from_st] = next_station_id
                        station_id_to_name[next_station_id] = from_st
                        next_station_id += 1

                    if to_st not in station_name_to_id:
                        station_name_to_id[to_st] = next_station_id
                        station_id_to_name[next_station_id] = to_st
                        next_station_id += 1

                    if vehicle not in vehicle_name_to_id:
                        vehicle_name_to_id[vehicle] = next_vehicle_id
                        vehicle_id_to_name[next_vehicle_id] = vehicle
                        next_vehicle_id += 1

                    new_cruise = Cruise(station_name_to_id[from_st], station_name_to_id[to_st], vehicle_name_to_id[vehicle], time_, cost_)
                    graph.insertCruise(new_cruise)

    except IOError:
        want_to_exit = True
        #log << "Проблема с файлом графа => завершение работы программы" << std::endl

    # "Красивая" распечатка графа для отладки
    #
    # for k, v in graph.graph.items():
    #     print(f'{station_id_to_name[k]}: ', end='')
    #     for pk, pv in v.items():
    #         print(station_id_to_name[pk], end='')
    #         cruises = pv
    #         for cruise in cruises:
    #             print(f' ({station_id_to_name[cruise.from_id]} {station_id_to_name[cruise.to_id]} {vehicle_id_to_name[cruise.vehicle_id]} ', end='')
    #             print(f'{cruise.cruise_time} {cruise.cruise_cost}), ', end='')
    #     print()

    stdscr = curses.initscr()
    stdscr.scrollok(True)
    stdscr.keypad(True)
    curses.noecho()

    # while (!want_to_exit)
    # {
    #     uint32_t current_item_index = 0;
    #     bool choice_made = false;       
 
    #     const char *choices[OPTIONS_NUM] = {"Нахождение пути минимальной стоимости среди кратчайших путей между двумя городами",
    #                                 "Нахождение пути минимальной стоимости между двумя городами",
    #                                 "Нахождение пути между двумя городами с минимальным числом пересадок",
    #                                 "Нахождение городов, достижимых из города отправления не более чем за лимит стоимости, и путей к ним",
    #                                 "Нахождение городов, достижимых из города отправления не более чем за лимит времени, и путей к ним",
    #                                 "Выйти из программы"};

    #     while (!choice_made)
    #     {
    #         clear();
    #         curs_set(0);
    #         addstr("Выберите желаемый режим работы программы:\n\n");
    #         refresh();
            
    #         for (uint32_t i = 0; i < OPTIONS_NUM; i++)
    #         {
    #             if (i == current_item_index)
    #             {
    #                 attron(A_STANDOUT);
    #                 printw("%s\n", choices[i]);
    #                 attroff(A_STANDOUT);
    #             }
    #             else
    #             {
    #                 printw("%s\n", choices[i]);
    #             }
    #             refresh();
    #         }

    #         switch (getch())
    #         {
    #             case KEY_UP:
    #             {
    #                 if (current_item_index > 0)
    #                 {
    #                     current_item_index--; 
    #                 }
    #                 else
    #                 {
    #                     current_item_index = OPTIONS_NUM -1;
    #                 }
    #                 break;
    #             }

    #             case KEY_DOWN:
    #             {
    #                 if (current_item_index < OPTIONS_NUM - 1)
    #                 {
    #                     current_item_index++;
    #                 }
    #                 else
    #                 {
    #                     current_item_index = 0;
    #                 }
    #                 break;
    #             }
                    
    #             case (int)'\n':
    #             {
    #                 choice_made = true;
    #                 break;
    #             }

    #             default:
    #             {
    #                 break;
    #             }
    #         }
    #     }

    #     log << "Выбран режим: " << choices[current_item_index] << std::endl;

    #     std::unordered_set<uint32_t> vehicles_types;

    #     if (current_item_index >= 0 && current_item_index <= OPTIONS_NUM - 2)
    #     {
    #         bool vehicles_chosen = false;
    #         uint32_t current_vehicle_id = 0;
    #         char choose_sym = '*';

    #         while (!vehicles_chosen)
    #         {
    #             clear();
    #             curs_set(0);
    #             addstr("Выберите подходящие виды транспорта:\n\n");
    #             refresh();
                
    #             for (uint32_t vehicle_id = 0; vehicle_id < next_vehicle_id; vehicle_id++)
    #             {
    #                 if (vehicle_id == current_vehicle_id)
    #                 {
    #                     attron(A_STANDOUT);
    #                 }
    #                 if (vehicles_types.find(vehicle_id) != vehicles_types.end())
    #                 {
    #                     printw("%c %s\n", choose_sym, vehicle_id_to_name[vehicle_id].c_str());
    #                 }
    #                 else
    #                 {
    #                     printw("  %s\n", vehicle_id_to_name[vehicle_id].c_str());
    #                 }
    #                 refresh();
    #                 if (vehicle_id == current_vehicle_id)
    #                 {
    #                     attroff(A_STANDOUT);
    #                 }
    #             }
    #             addstr("\n");
    #             refresh();
    #             if (current_vehicle_id == next_vehicle_id)
    #             {
    #                 attron(A_STANDOUT);
    #             }
    #             addstr("Далее");
    #             if (current_vehicle_id == next_vehicle_id)
    #             {
    #                 attroff(A_STANDOUT);
    #             }
    #             refresh();

    #             switch (getch())
    #             {
    #                 case KEY_UP:
    #                 {
    #                     if (current_vehicle_id > 0)
    #                     {
    #                         current_vehicle_id--; 
    #                     }
    #                     else
    #                     {
    #                         current_vehicle_id = next_vehicle_id;
    #                     }
    #                     break;
    #                 }

    #                 case KEY_DOWN:
    #                 {
    #                     if (current_vehicle_id < next_vehicle_id)
    #                     {
    #                         current_vehicle_id++;
    #                     }
    #                     else
    #                     {
    #                         current_vehicle_id = 0;
    #                     }
    #                     break;
    #                 }
                        
    #                 case (int)'\n':
    #                 {
    #                     if (current_vehicle_id == next_vehicle_id)
    #                     {
    #                         vehicles_chosen = true;
    #                     }
    #                     else if (vehicles_types.find(current_vehicle_id) == vehicles_types.end())
    #                     {
    #                         vehicles_types.insert(current_vehicle_id);
    #                     }
    #                     else
    #                     {
    #                         vehicles_types.erase(current_vehicle_id);
    #                     }
    #                     break;
    #                 }

    #                 default:
    #                 {
    #                     break;
    #                 }
    #             }
    #         }
    #     }

    #     if (current_item_index != WANT_TO_EXIT)
    #     {
    #         log << "Выбранные виды транспорта: ";
    #         for (auto vehicle : vehicles_types)
    #         {
    #             log << vehicle_id_to_name[vehicle] << ", ";
    #         }
    #         log << std::endl;
    #     }

    #     echo();

        match current_item_index:
            case MINCOST_MINTIME_MODE:
                curses.clear()
                stdscr.addstr('Введите станцию отправления:\n')
                stdscr.refresh()
                curses.curs_set(1)
                station_from = stdscr.getstr()
                while station_from not in station_name_to_id:
                    curses.clear()
                    stdscr.addstr('Введена недопустимая станция отправления. Введите станцию отправления:\n')
                    stdscr.refresh()
                    curses.curs_set(1)
                    station_from = stdscr.getstr()
                #log << "Станция отправления: " << station_from << std::endl
                curses.clear()
                stdscr.addstr('Введите станцию прибытия:\n')
                stdscr.refresh()
                curses.curs_set(1)
                station_to = stdscr.getstr()
                while station_to not in station_name_to_id:
                    curses.clear()
                    stdscr.addstr('Введена недопустимая станция прибытия. Введите станцию прибытия:\n')
                    stdscr.refresh()
                    curses.curs_set(1)
                    station_to = stdscr.getstr()
                #log << "Станция прибытия: " << station_to << std::endl
                from_id = station_name_to_id[station_from]
                to_id = station_name_to_id[station_to]

                #auto start_operation = std::chrono::high_resolution_clock::now()
                
                d, extra, p = dijkstra_extra_cond(from_id, next_station_id, graph, 0, vehicles_types)

                trip = Trip()
                current_station = to_id
                if d[to_id] < INF:
                    while current_station != from_id:
                        next_cruise = p[current_station]
                        trip += next_cruise
                        current_station = next_cruise.from_id
                #auto end_operation = std::chrono::high_resolution_clock::now()
                #std::chrono::duration<double> operation_time = end_operation - start_operation
                #log << "Время выполнения запроса: " << operation_time.count() << " сек." << std::endl

                #if (getrusage(RUSAGE_SELF, &rusage) != -1)
                #{
                    #log << "Max RSS: " << (double)rusage.ru_maxrss << " KiB" << std::endl
                #}
                
                if trip.cruises_num > 0:
                    for count in range(1, trip.cruises_num + 1):
                        cruise = trip[count - 1]
                        from_st = station_id_to_name[cruise.from_id]
                        to_st = station_id_to_name[cruise.to_id]
                        vehicle = vehicle_id_to_name[cruise.vehicle_id]
                        time_ = cruise.cruise_time
                        cost_ = cruise.cruise_cost
                        stdscr.addstr(f'{count}) Из: {from_st}, в: {to_st}, транспорт: {vehicle}, время: {time_}, стоимость: {cost_}\n')
                        stdscr.refresh()
                        #log << count << ") Из: " << from << ", в: " << to << ", транспорт: " << vehicle
                        #log << ", время: " << time_ << ", стоимость: " << cost_ << std::endl
                    stdscr.addstr(f'Время пути: {trip.trip_time}\n')
                    stdscr.refresh()
                    #log << "Время пути: " << trip.trip_time << std::endl
                    stdscr.addstr(f'Стоимость пути: {trip.trip_cost}\n')
                    stdscr.refresh()
                    #log << "Стоимость пути: " << trip.trip_cost << std::endl
                    #log << std::endl
                else:
                    stdscr.addstr('С помощью данных видов транспорта город прибытия не достижим из города отправления\n')
                    #log << "С помощью данных видов транспорта город прибытия не достижим из города отправления" << std::endl << std::endl
                    stdscr.refresh()
                stdscr.addstr('Нажмите любую клавишу для перехода в меню\n')
                stdscr.refresh()
                curses.curs_set(0)
                curses.getch()
                break

            # case MINCOST_MODE:
            #     clear();
            #     char station_from_char[100];
            #     addstr("Введите станцию отправления:\n");
            #     refresh();
            #     curs_set(1);
            #     getnstr(station_from_char, 100);
            #     std::string station_from(station_from_char);
            #     while (station_name_to_id.find(station_from) == station_name_to_id.end())
            #     {
            #         clear();
            #         addstr("Введена недопустимая станция отправления. Введите станцию отправления:\n");
            #         refresh();
            #         curs_set(1);
            #         getnstr(station_from_char, 100);
            #         station_from = station_from_char;
            #     }
            #     #log << "Станция отправления: " << station_from << std::endl;
            #     clear();
            #     char station_to_char[100];
            #     addstr("Введите станцию прибытия:\n");
            #     refresh();
            #     curs_set(1);
            #     getnstr(station_to_char, 100);
            #     std::string station_to(station_to_char);
            #     while (station_name_to_id.find(station_to) == station_name_to_id.end())
            #     {
            #         clear();
            #         addstr("Введена недопустимая станция прибытия. Введите станцию прибытия:\n");
            #         refresh();
            #         curs_set(1);
            #         getnstr(station_to_char, 100);
            #         station_to = station_to_char;
            #     }
            #     #log << "Станция прибытия: " << station_to << std::endl;
            #     uint32_t from_id, to_id;
            #     from_id = station_name_to_id[station_from];
            #     to_id = station_name_to_id[station_to];

            #     auto start_operation = std::chrono::high_resolution_clock::now();
                
            #     d, p = dijkstra(from_id, next_station_id, graph, 1, vehicles_types);

            #     Trip trip;
            #     uint32_t current_station = to_id;
            #     if (d[to_id] < INF)
            #     {
            #         while (current_station != from_id)
            #         {
            #             Cruise next_cruise = p[current_station];
            #             trip += next_cruise;
            #             current_station = next_cruise.from_id;
            #         }
            #     }
            #     auto end_operation = std::chrono::high_resolution_clock::now();
            #     std::chrono::duration<double> operation_time = end_operation - start_operation;
            #     #log << "Время выполнения запроса: " << operation_time.count() << " сек." << std::endl;

            #     if (getrusage(RUSAGE_SELF, &rusage) != -1)
            #     {
            #         #log << "Max RSS: " << (double)rusage.ru_maxrss << " KiB" << std::endl;
            #     }
                
            #     if (trip.cruises_num > 0)
            #     {
            #         for (uint32_t count = 1; count <= trip.cruises_num; count++)
            #         {
            #             Cruise cruise = trip[count - 1];
            #             std::string from = station_id_to_name[cruise.from_id];
            #             std::string to = station_id_to_name[cruise.to_id];
            #             std::string vehicle = vehicle_id_to_name[cruise.vehicle_id];
            #             uint32_t time_ = cruise.cruise_time;
            #             uint32_t cost_ = cruise.cruise_cost;
            #             printw("%i) Из: %s, в: %s, транспорт: %s, время: %i, стоимость: %i\n", count, from.c_str(), to.c_str(), vehicle.c_str(), time_, cost_);
            #             refresh();
            #             #log << count << ") Из: " << from << ", в: " << to << ", транспорт: " << vehicle;
            #             #log << ", время: " << time_ << ", стоимость: " << cost_ << std::endl;
            #         }
            #         printw("Время пути: %i\n", trip.trip_time);
            #         refresh();
            #         #log << "Время пути: " << trip.trip_time << std::endl;
            #         printw("Стоимость пути: %i\n", trip.trip_cost);
            #         refresh();
            #         #log << "Стоимость пути: " << trip.trip_cost << std::endl;
            #         #log << std::endl;
            #     }
            #     else
            #     {
            #         addstr("С помощью данных видов транспорта город прибытия не достижим из города отправления\n");
            #         #log << "С помощью данных видов транспорта город прибытия не достижим из города отправления" << std::endl << std::endl;
            #         refresh();
            #     }
            #     addstr("Нажмите любую клавишу для перехода в меню\n");
            #     refresh();
            #     curs_set(0);
            #     getch();
            #     break

            # case MINSTATIONSNUM_MODE:
            #     clear();
            #     char station_from_char[100];
            #     addstr("Введите станцию отправления:\n");
            #     refresh();
            #     curs_set(1);
            #     getnstr(station_from_char, 100);
            #     std::string station_from(station_from_char);
            #     while (station_name_to_id.find(station_from) == station_name_to_id.end())
            #     {
            #         clear();
            #         addstr("Введена недопустимая станция отправления. Введите станцию отправления:\n");
            #         refresh();
            #         curs_set(1);
            #         getnstr(station_from_char, 100);
            #         station_from = station_from_char;
            #     }
            #     #log << "Станция отправления: " << station_from << std::endl;
            #     clear();
            #     char station_to_char[100];
            #     addstr("Введите станцию прибытия:\n");
            #     refresh();
            #     curs_set(1);
            #     getnstr(station_to_char, 100);
            #     std::string station_to(station_to_char);
            #     while (station_name_to_id.find(station_to) == station_name_to_id.end())
            #     {
            #         clear();
            #         addstr("Введена недопустимая станция прибытия. Введите станцию прибытия:\n");
            #         refresh();
            #         curs_set(1);
            #         getnstr(station_to_char, 100);
            #         station_to = station_to_char;
            #     }
            #     #log << "Станция прибытия: " << station_to << std::endl;
            #     uint32_t from_id, to_id;
            #     from_id = station_name_to_id[station_from];
            #     to_id = station_name_to_id[station_to];

            #     auto start_operation = std::chrono::high_resolution_clock::now();
                
            #     d, p = bfs(from_id, next_station_id, graph, vehicles_types)

            #     Trip trip;
            #     uint32_t current_station = to_id;
            #     if (d[to_id] < INF)
            #     {
            #         while (current_station != from_id)
            #         {
            #             Cruise next_cruise = p[current_station];
            #             trip += next_cruise;
            #             current_station = next_cruise.from_id;
            #         }
            #     }
            #     auto end_operation = std::chrono::high_resolution_clock::now();
            #     std::chrono::duration<double> operation_time = end_operation - start_operation;
            #     #log << "Время выполнения запроса: " << operation_time.count() << " сек." << std::endl;

            #     if (getrusage(RUSAGE_SELF, &rusage) != -1)
            #     {
            #         #log << "Max RSS: " << (double)rusage.ru_maxrss << " KiB" << std::endl;
            #     }
                
            #     if (trip.cruises_num > 0)
            #     {
            #         for (uint32_t count = 1; count <= trip.cruises_num; count++)
            #         {
            #             Cruise cruise = trip[count - 1];
            #             std::string from = station_id_to_name[cruise.from_id];
            #             std::string to = station_id_to_name[cruise.to_id];
            #             std::string vehicle = vehicle_id_to_name[cruise.vehicle_id];
            #             uint32_t time_ = cruise.cruise_time;
            #             uint32_t cost_ = cruise.cruise_cost;
            #             printw("%i) Из: %s, в: %s, транспорт: %s, время: %i, стоимость: %i\n", count, from.c_str(), to.c_str(), vehicle.c_str(), time_, cost_);
            #             refresh();
            #             #log << count << ") Из: " << from << ", в: " << to << ", транспорт: " << vehicle;
            #             #log << ", время: " << time_ << ", стоимость: " << cost_ << std::endl;
            #         }
            #         printw("Время пути: %i\n", trip.trip_time);
            #         refresh();
            #         #log << "Время пути: " << trip.trip_time << std::endl;
            #         printw("Стоимость пути: %i\n", trip.trip_cost);
            #         refresh();
            #         #log << "Стоимость пути: " << trip.trip_cost << std::endl;
            #         #log << std::endl;
            #     }
            #     else
            #     {
            #         addstr("С помощью данных видов транспорта город прибытия не достижим из города отправления\n");
            #         #log << "С помощью данных видов транспорта город прибытия не достижим из города отправления" << std::endl << std::endl;
            #         refresh();
            #     }
            #     addstr("Нажмите любую клавишу для перехода в меню\n");
            #     refresh();
            #     curs_set(0);
            #     getch();
            #     break

            # case LIMITCOST_MODE:
            #     clear();
            #     char station_from_char[100];
            #     addstr("Введите станцию отправления:\n");
            #     refresh();
            #     curs_set(1);
            #     getnstr(station_from_char, 100);
            #     std::string station_from(station_from_char);
            #     while (station_name_to_id.find(station_from) == station_name_to_id.end())
            #     {
            #         clear();
            #         addstr("Введена недопустимая станция отправления. Введите станцию отправления:\n");
            #         refresh();
            #         curs_set(1);
            #         getnstr(station_from_char, 100);
            #         station_from = station_from_char;
            #     }
            #     #log << "Станция отправления: " << station_from << std::endl;
            #     clear();
            #     char limit_cost_char[100];
            #     addstr("Введите лимит стоимости:\n");
            #     refresh();
            #     curs_set(1);
            #     getnstr(limit_cost_char, 100);
            #     std::string limit_cost_str(limit_cost_char);               
            #     while (limit_cost_str == "" || !is_digits(limit_cost_str) || stoi(limit_cost_str) <= 0)
            #     {
            #         clear();
            #         addstr("Введена недопустимый лимит стоимости. Введите лимит стоимости:\n");
            #         refresh();
            #         curs_set(1);
            #         getnstr(limit_cost_char, 100);
            #         limit_cost_str = limit_cost_char;
            #     }
            #     #log << "Лимит стоимости: " << limit_cost_str << std::endl;
            #     uint32_t from_id, limit_cost;
            #     limit_cost = stoi(limit_cost_str);
            #     from_id = station_name_to_id[station_from];

            #     auto start_operation = std::chrono::high_resolution_clock::now();

            #     d, p = dijkstra(from_id, next_station_id, graph, 1, vehicles_types)

            #     std::map<uint32_t, Trip> trips_map;
            #     for (uint32_t i = 0; i < next_station_id; i++)
            #     {
            #         if (i != from_id && d[i] <= limit_cost)
            #         {
            #             Trip trip;
            #             uint32_t current_station = i;
            #             while (current_station != from_id)
            #             {
            #                 Cruise next_cruise = p[current_station];
            #                 trip += next_cruise;
            #                 current_station = next_cruise.from_id;
            #             }
            #             trips_map[i] = trip;
            #         }
            #     }
            #     auto end_operation = std::chrono::high_resolution_clock::now();
            #     std::chrono::duration<double> operation_time = end_operation - start_operation;
            #     #log << "Время выполнения запроса: " << operation_time.count() << " сек." << std::endl;

            #     if (getrusage(RUSAGE_SELF, &rusage) != -1)
            #     {
            #         #log << "Max RSS: " << (double)rusage.ru_maxrss << " KiB" << std::endl;
            #     }

            #     if (!trips_map.empty())
            #     {
            #         for (auto station_from_and_trip : trips_map)
            #         {
            #             std::string station_from = station_id_to_name[station_from_and_trip.first];
            #             Trip trip = station_from_and_trip.second;

            #             printw("До станции '%s':\n", station_from.c_str());
            #             refresh();
            #             #log << "До станции '" << station_from << "':" << std::endl;

            #             for (uint32_t count = 1; count <= trip.cruises_num; count++)
            #             {
            #                 Cruise cruise = trip[count - 1];
            #                 std::string from = station_id_to_name[cruise.from_id];
            #                 std::string to = station_id_to_name[cruise.to_id];
            #                 std::string vehicle = vehicle_id_to_name[cruise.vehicle_id];
            #                 uint32_t time_ = cruise.cruise_time;
            #                 uint32_t cost_ = cruise.cruise_cost;
            #                 printw("%i) Из: %s, в: %s, транспорт: %s, время: %i, стоимость: %i\n", count, from.c_str(), to.c_str(), vehicle.c_str(), time_, cost_);
            #                 refresh();
            #                 #log << count << ") Из: " << from << ", в: " << to << ", транспорт: " << vehicle;
            #                 #log << ", время: " << time_ << ", стоимость: " << cost_ << std::endl;
            #             }
            #             printw("Время пути: %i\n", trip.trip_time);
            #             refresh();
            #             #log << "Время пути: " << trip.trip_time << std::endl;
            #             printw("Стоимость пути: %i\n", trip.trip_cost);
            #             refresh();
            #             #log << "Стоимость пути: " << trip.trip_cost << std::endl;
            #         }
            #         #log << std::endl;
            #     }
            #     else
            #     {
            #         addstr("С помощью данных видов транспорта ни один из городов не достижим из города отправления за данный лимит стоимости\n");
            #         #log << "С помощью данных видов транспорта ни один из городов не достижим из города отправления за данный лимит стоимости";
            #         #log << std::endl << std::endl;
            #         refresh();
            #     }
            #     addstr("Нажмите любую клавишу для перехода в меню\n");
            #     refresh();
            #     curs_set(0);
            #     getch();
            #     break

            # case LIMITTIME_MODE:
            #     clear();
            #     char station_from_char[100];
            #     addstr("Введите станцию отправления:\n");
            #     refresh();
            #     curs_set(1);
            #     getnstr(station_from_char, 100);
            #     std::string station_from(station_from_char);
            #     while (station_name_to_id.find(station_from) == station_name_to_id.end())
            #     {
            #         clear();
            #         addstr("Введена недопустимая станция отправления. Введите станцию отправления:\n");
            #         refresh();
            #         curs_set(1);
            #         getnstr(station_from_char, 100);
            #         station_from = station_from_char;
            #     }
            #     #log << "Станция отправления: " << station_from << std::endl;
            #     clear();
            #     char limit_time_char[100];
            #     addstr("Введите лимит времени:\n");
            #     refresh();
            #     curs_set(1);
            #     getnstr(limit_time_char, 100);
            #     std::string limit_time_str(limit_time_char);               
            #     while (limit_time_str == "" || !is_digits(limit_time_str) || stoi(limit_time_str) <= 0)
            #     {
            #         clear();
            #         addstr("Введена недопустимый лимит времени. Введите лимит времени:\n");
            #         refresh();
            #         curs_set(1);
            #         getnstr(limit_time_char, 100);
            #         limit_time_str = limit_time_char;
            #     }
            #     #log << "Лимит времени: " << limit_time_str << std::endl;
            #     uint32_t from_id, limit_time;
            #     limit_time = stoi(limit_time_str);
            #     from_id = station_name_to_id[station_from];

            #     auto start_operation = std::chrono::high_resolution_clock::now();

            #     dijkstra(from_id, next_station_id, graph, 0, vehicles_types)

            #     std::map<uint32_t, Trip> trips_map;
            #     for (uint32_t i = 0; i < next_station_id; i++)
            #     {
            #         if (i != from_id && d[i] <= limit_time)
            #         {
            #             Trip trip;
            #             uint32_t current_station = i;
            #             while (current_station != from_id)
            #             {
            #                 Cruise next_cruise = p[current_station];
            #                 trip += next_cruise;
            #                 current_station = next_cruise.from_id;
            #             }
            #             trips_map[i] = trip;
            #         }
            #     }
            #     auto end_operation = std::chrono::high_resolution_clock::now();
            #     std::chrono::duration<double> operation_time = end_operation - start_operation;
            #     #log << "Время выполнения запроса: " << operation_time.count() << " сек." << std::endl;

            #     if (getrusage(RUSAGE_SELF, &rusage) != -1)
            #     {
            #         #log << "Max RSS: " << (double)rusage.ru_maxrss << " KiB" << std::endl;
            #     }

            #     if (!trips_map.empty())
            #     {
            #         for (auto station_from_and_trip : trips_map)
            #         {
            #             std::string station_from = station_id_to_name[station_from_and_trip.first];
            #             Trip trip = station_from_and_trip.second;

            #             printw("До станции '%s':\n", station_from.c_str());
            #             refresh();
            #             #log << "До станции '" << station_from << "':" << std::endl;

            #             for (uint32_t count = 1; count <= trip.cruises_num; count++)
            #             {
            #                 Cruise cruise = trip[count - 1];
            #                 std::string from = station_id_to_name[cruise.from_id];
            #                 std::string to = station_id_to_name[cruise.to_id];
            #                 std::string vehicle = vehicle_id_to_name[cruise.vehicle_id];
            #                 uint32_t time_ = cruise.cruise_time;
            #                 uint32_t cost_ = cruise.cruise_cost;
            #                 printw("%i) Из: %s, в: %s, транспорт: %s, время: %i, стоимость: %i\n", count, from.c_str(), to.c_str(), vehicle.c_str(), time_, cost_);
            #                 refresh();
            #                 #log << count << ") Из: " << from << ", в: " << to << ", транспорт: " << vehicle;
            #                 #log << ", время: " << time_ << ", стоимость: " << cost_ << std::endl;
            #             }
            #             printw("Время пути: %i\n", trip.trip_time);
            #             refresh();
            #             #log << "Время пути: " << trip.trip_time << std::endl;
            #             printw("Стоимость пути: %i\n", trip.trip_cost);
            #             refresh();
            #             #log << "Стоимость пути: " << trip.trip_cost << std::endl;
            #         }
            #         #log << std::endl;
            #     }
            #     else
            #     {
            #         addstr("С помощью данных видов транспорта ни один из городов не достижим из города отправления за данный лимит времени\n");
            #         #log << "С помощью данных видов транспорта ни один из городов не достижим из города отправления за данный лимит времени";
            #         #log << std::endl << std::endl;
            #         refresh();
            #     }
            #     addstr("Нажмите любую клавишу для перехода в меню\n");
            #     refresh();
            #     curs_set(0);
            #     getch();
            #     break

            case WANT_TO_EXIT:
                want_to_exit = True
                break

            default:
                break
    # }

    curses.endwin()

    # auto end_program = std::chrono::high_resolution_clock::now();
    # std::chrono::duration<double> program_duration = end_program - start_program;
    # log << "Время выполнения программы: " << program_duration.count() << " сек." << std::endl;

    # if (getrusage(RUSAGE_SELF, &rusage) != -1)
    # {
    #     log << "Max RSS: " << (double)rusage.ru_maxrss << " KiB" << std::endl << std::endl;
    # }


if __name__ == '__main__':
    main()