from task_graphs_py.classes import INF, Cruise, Trip, CruisesGraph
from task_graphs_py.algorithms import bfs, dijkstra, dijkstra_extra_cond

import curses
import sys
import os
from datetime import datetime
from resource import getrusage, RUSAGE_SELF


OPTIONS_NUM = 6

MINCOST_MINTIME_MODE = 0
MINCOST_MODE = 1
MINSTATIONSNUM_MODE = 2
LIMITCOST_MODE = 3
LIMITTIME_MODE = 4
WANT_TO_EXIT = 5


def main(stdscr):
    # auto start_program = std::chrono::high_resolution_clock::now();

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
    log = open(os.getcwd() + '/task_graphs_py/log.txt', 'a', encoding='utf-8')
    print(datetime.now(), file=log)

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
        print('Проблема с файлом графа => завершение работы программы', file=log)

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

    while not want_to_exit:
        current_item_index = 0
        choice_made = False       
 
        choices = ['Нахождение пути минимальной стоимости среди кратчайших путей между двумя городами',
                   'Нахождение пути минимальной стоимости между двумя городами',
                   'Нахождение пути между двумя городами с минимальным числом пересадок',
                   'Нахождение городов, достижимых из города отправления не более чем за лимит стоимости, и путей к ним',
                   'Нахождение городов, достижимых из города отправления не более чем за лимит времени, и путей к ним',
                   'Выйти из программы']

        while not choice_made:
            stdscr.clear()
            curses.curs_set(0)
            stdscr.addstr('Выберите желаемый режим работы программы:\n\n')
            stdscr.refresh()
            
            for i in range(OPTIONS_NUM):
                if i == current_item_index:
                    stdscr.attron(curses.A_STANDOUT)
                    stdscr.addstr(f'{choices[i]}\n')
                    stdscr.attroff(curses.A_STANDOUT)
                else:
                    stdscr.addstr(f'{choices[i]}\n')
                stdscr.refresh()

            key = stdscr.getch()
            if key == curses.KEY_UP:
                if current_item_index > 0:
                    current_item_index -= 1
                else:
                    current_item_index = OPTIONS_NUM - 1
            elif key == curses.KEY_DOWN:
                if current_item_index < OPTIONS_NUM - 1:
                    current_item_index += 1
                else:
                    current_item_index = 0
            elif key == curses.KEY_ENTER or key == 10 or key == 13:
                choice_made = True

        print(f'Выбран режим: {choices[current_item_index]}', file=log)

        vehicles_types = set()

        if current_item_index >= 0 and current_item_index <= OPTIONS_NUM - 2:
            vehicles_chosen = False
            current_vehicle_id = 0
            choose_sym = '*'

            while not vehicles_chosen:
                stdscr.clear()
                curses.curs_set(0)
                stdscr.addstr('Выберите подходящие виды транспорта:\n\n')
                stdscr.refresh()
                
                for vehicle_id in range(next_vehicle_id):
                    if vehicle_id == current_vehicle_id:
                        stdscr.attron(curses.A_STANDOUT)
                    if vehicle_id in vehicles_types:
                        stdscr.addstr(f'{choose_sym} {vehicle_id_to_name[vehicle_id]}\n')
                    else:
                        stdscr.addstr(f'  {vehicle_id_to_name[vehicle_id]}\n')
                    stdscr.refresh()
                    if vehicle_id == current_vehicle_id:
                        stdscr.attroff(curses.A_STANDOUT)
                stdscr.addstr('\n')
                stdscr.refresh()
                if current_vehicle_id == next_vehicle_id:
                    stdscr.attron(curses.A_STANDOUT)
                stdscr.addstr('Далее')
                if current_vehicle_id == next_vehicle_id:
                    stdscr.attroff(curses.A_STANDOUT)
                stdscr.refresh()

                key = stdscr.getch()
                if key == curses.KEY_UP:
                    if current_vehicle_id > 0:
                        current_vehicle_id -= 1
                    else:
                        current_vehicle_id = next_vehicle_id
                elif key == curses.KEY_DOWN:
                    if current_vehicle_id < next_vehicle_id:
                        current_vehicle_id += 1
                    else:
                        current_vehicle_id = 0
                        
                elif key == curses.KEY_ENTER or key == 10 or key == 13:
                    if current_vehicle_id == next_vehicle_id:
                        vehicles_chosen = True
                    elif current_vehicle_id not in vehicles_types:
                        vehicles_types.add(current_vehicle_id)
                    else:
                        vehicles_types.remove(current_vehicle_id)

        #if current_item_index != WANT_TO_EXIT:
            #log << "Выбранные виды транспорта: "
            #for vehicle in vehicles_types:
                #log << vehicle_id_to_name[vehicle] << ", "
            #log << std::endl

        curses.echo()

        if current_item_index == MINCOST_MINTIME_MODE:
            stdscr.clear()
            stdscr.addstr('Введите станцию отправления:\n')
            stdscr.refresh()
            curses.curs_set(1)
            station_from = str(stdscr.getstr(), 'utf-8', errors='ignore')
            while station_from not in station_name_to_id:
                stdscr.clear()
                stdscr.addstr('Введена недопустимая станция отправления. Введите станцию отправления:\n')
                stdscr.refresh()
                curses.curs_set(1)
                station_from = str(stdscr.getstr(), 'utf-8', errors='ignore')
            print(f'Станция отправления: {station_from}', file=log)
            stdscr.clear()
            stdscr.addstr('Введите станцию прибытия:\n')
            stdscr.refresh()
            curses.curs_set(1)
            station_to = str(stdscr.getstr(), 'utf-8', errors='ignore')
            while station_to not in station_name_to_id:
                stdscr.clear()
                stdscr.addstr('Введена недопустимая станция прибытия. Введите станцию прибытия:\n')
                stdscr.refresh()
                curses.curs_set(1)
                station_to = str(stdscr.getstr(), 'utf-8', errors='ignore')
            print(f'Станция прибытия: {station_to}', file=log)
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
            stdscr.getch()

        # elif current_item_index == MINCOST_MODE:
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

        # elif current_item_index == MINSTATIONSNUM_MODE:
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

        # elif current_item_index == LIMITCOST_MODE:
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

        # elif current_item_index == LIMITTIME_MODE:
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

        elif current_item_index == WANT_TO_EXIT:
            want_to_exit = True

    curses.endwin()

    # auto end_program = std::chrono::high_resolution_clock::now();
    # std::chrono::duration<double> program_duration = end_program - start_program;
    # log << "Время выполнения программы: " << program_duration.count() << " сек." << std::endl;

    print(f'Max RSS: {getrusage(RUSAGE_SELF).ru_maxrss} KiB\n', file=log)

    log.close()


if __name__ == '__main__':
    curses.wrapper(main)