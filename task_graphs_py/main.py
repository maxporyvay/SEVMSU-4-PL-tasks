#!/usr/bin/python3

from classes import INF, Cruise, Trip, CruisesGraph
from algorithms import bfs, dijkstra, dijkstra_extra_cond

import curses
import sys
import os
from datetime import datetime
from time import time
from resource import getrusage, RUSAGE_SELF


OPTIONS_NUM = 6

MINCOST_MINTIME_MODE = 0
MINCOST_MODE = 1
MINSTATIONSNUM_MODE = 2
LIMITCOST_MODE = 3
LIMITTIME_MODE = 4
WANT_TO_EXIT = 5


def main(stdscr):
    start_program = time()

    station_name_to_id = {}
    station_id_to_name = {}
    next_station_id = 0

    vehicle_name_to_id = {}
    vehicle_id_to_name = {}
    next_vehicle_id = 0

    graph = CruisesGraph()

    filename = os.getcwd() + '/' + sys.argv[1]

    want_to_exit = False
    log = open(str(os.path.join(os.path.dirname(__file__), '../log.txt')), 'a', encoding='utf-8')
    print('PYTHON', file=log)
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

        if current_item_index != WANT_TO_EXIT:
            print('Выбранные виды транспорта: ', file=log, end='')
            for vehicle in vehicles_types:
                print(f'{vehicle_id_to_name[vehicle]}, ', end='', file=log)
            print(file=log)

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

            start_operation = time()
            
            d, extra, p = dijkstra_extra_cond(from_id, next_station_id, graph, 0, vehicles_types)

            trip = Trip()
            current_station = to_id
            if d[to_id] < INF:
                while current_station != from_id:
                    next_cruise = p[current_station]
                    trip += next_cruise
                    current_station = next_cruise.from_id
            end_operation = time()
            print(f'Время выполнения запроса: {end_operation - start_operation} сек.', file=log)

            print(f'Max RSS: {getrusage(RUSAGE_SELF).ru_maxrss} KiB\n', file=log)
            
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
                    print(f'{count}) Из: {from_st}, в: {to_st}, транспорт: {vehicle}, время: {time_}, стоимость: {cost_}', file=log)
                stdscr.addstr(f'Время пути: {trip.trip_time}\n')
                stdscr.refresh()
                print(f'Время пути: {trip.trip_time}', file=log)
                stdscr.addstr(f'Стоимость пути: {trip.trip_cost}\n')
                stdscr.refresh()
                print(f'Стоимость пути: {trip.trip_cost}', file=log)
                print(file=log)
            else:
                stdscr.addstr('С помощью данных видов транспорта город прибытия не достижим из города отправления\n')
                print("С помощью данных видов транспорта город прибытия не достижим из города отправления\n", file=log)
                stdscr.refresh()
            stdscr.addstr('Нажмите любую клавишу для перехода в меню\n')
            stdscr.refresh()
            curses.curs_set(0)
            stdscr.getch()

        elif current_item_index == MINCOST_MODE:
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

            start_operation = time()
            
            d, p = dijkstra(from_id, next_station_id, graph, 1, vehicles_types)

            trip = Trip()
            current_station = to_id
            if d[to_id] < INF:
                while current_station != from_id:
                    next_cruise = p[current_station]
                    trip += next_cruise
                    current_station = next_cruise.from_id
            end_operation = time()
            print(f'Время выполнения запроса: {end_operation - start_operation} сек.', file=log)

            print(f'Max RSS: {getrusage(RUSAGE_SELF).ru_maxrss} KiB\n', file=log)
            
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
                    print(f'{count}) Из: {from_st}, в: {to_st}, транспорт: {vehicle}, время: {time_}, стоимость: {cost_}', file=log)
                stdscr.addstr(f'Время пути: {trip.trip_time}\n')
                stdscr.refresh()
                print(f'Время пути: {trip.trip_time}', file=log)
                stdscr.addstr(f'Стоимость пути: {trip.trip_cost}\n')
                stdscr.refresh()
                print(f'Стоимость пути: {trip.trip_cost}', file=log)
                print(file=log)
            else:
                stdscr.addstr('С помощью данных видов транспорта город прибытия не достижим из города отправления\n')
                print("С помощью данных видов транспорта город прибытия не достижим из города отправления\n", file=log)
                stdscr.refresh()
            stdscr.addstr('Нажмите любую клавишу для перехода в меню\n')
            stdscr.refresh()
            curses.curs_set(0)
            stdscr.getch()

        elif current_item_index == MINSTATIONSNUM_MODE:
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

            start_operation = time()
            
            d, p = bfs(from_id, next_station_id, graph, vehicles_types)

            trip = Trip()
            current_station = to_id
            if d[to_id] < INF:
                while current_station != from_id:
                    next_cruise = p[current_station]
                    trip += next_cruise
                    current_station = next_cruise.from_id
            end_operation = time()
            print(f'Время выполнения запроса: {end_operation - start_operation} сек.', file=log)

            print(f'Max RSS: {getrusage(RUSAGE_SELF).ru_maxrss} KiB\n', file=log)
            
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
                    print(f'{count}) Из: {from_st}, в: {to_st}, транспорт: {vehicle}, время: {time_}, стоимость: {cost_}', file=log)
                stdscr.addstr(f'Время пути: {trip.trip_time}\n')
                stdscr.refresh()
                print(f'Время пути: {trip.trip_time}', file=log)
                stdscr.addstr(f'Стоимость пути: {trip.trip_cost}\n')
                stdscr.refresh()
                print(f'Стоимость пути: {trip.trip_cost}', file=log)
                print(file=log)
            else:
                stdscr.addstr('С помощью данных видов транспорта город прибытия не достижим из города отправления\n')
                print("С помощью данных видов транспорта город прибытия не достижим из города отправления\n", file=log)
                stdscr.refresh()
            stdscr.addstr('Нажмите любую клавишу для перехода в меню\n')
            stdscr.refresh()
            curses.curs_set(0)
            stdscr.getch()

        elif current_item_index == LIMITCOST_MODE:
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
            stdscr.addstr('Введите лимит стоимости:\n')
            stdscr.refresh()
            curses.curs_set(1)
            limit_cost_str = str(stdscr.getstr(), 'utf-8', errors='ignore')         
            while limit_cost_str == '' or not limit_cost_str.isdigit() or int(limit_cost_str) <= 0:
                stdscr.clear()
                stdscr.addstr('Введите лимит стоимости:\n')
                stdscr.refresh()
                curses.curs_set(1)
                limit_cost_str = str(stdscr.getstr(), 'utf-8', errors='ignore')      
            print(f'Лимит стоимости: {limit_cost_str}', file=log)
            limit_cost = int(limit_cost_str)
            from_id = station_name_to_id[station_from]

            start_operation = time()

            d, p = dijkstra(from_id, next_station_id, graph, 1, vehicles_types)

            trips_map = {}
            for i in range(next_station_id):
                if i != from_id and d[i] <= limit_cost:
                    trip = Trip()
                    current_station = i
                    while current_station != from_id:
                        next_cruise = p[current_station]
                        trip += next_cruise
                        current_station = next_cruise.from_id
                    trips_map[i] = trip
            end_operation = time()
            print(f'Время выполнения запроса: {end_operation - start_operation} сек.', file=log)

            print(f'Max RSS: {getrusage(RUSAGE_SELF).ru_maxrss} KiB\n', file=log)

            if len(trips_map) > 0:
                for station_from_id, trip in trips_map.items():
                    station_from = station_id_to_name[station_from_id]

                    stdscr.addstr(f'До станции "{station_from}":\n')
                    stdscr.refresh()
                    print(f'До станции "{station_from}":', file=log)

                    for count in range(1, trip.cruises_num + 1):
                        cruise = trip[count - 1]
                        from_st = station_id_to_name[cruise.from_id]
                        to_st = station_id_to_name[cruise.to_id]
                        vehicle = vehicle_id_to_name[cruise.vehicle_id]
                        time_ = cruise.cruise_time
                        cost_ = cruise.cruise_cost
                        stdscr.addstr(f'{count}) Из: {from_st}, в: {to_st}, транспорт: {vehicle}, время: {time_}, стоимость: {cost_}\n')
                        stdscr.refresh()
                        print(f'{count}) Из: {from_st}, в: {to_st}, транспорт: {vehicle}, время: {time_}, стоимость: {cost_}', file=log)
                    stdscr.addstr(f'Время пути: {trip.trip_time}\n')
                    stdscr.refresh()
                    print(f'Время пути: {trip.trip_time}', file=log)
                    stdscr.addstr(f'Стоимость пути: {trip.trip_cost}\n')
                    stdscr.refresh()
                    print(f'Стоимость пути: {trip.trip_cost}', file=log)
                print(file=log)
            else:
                stdscr.addstr('С помощью данных видов транспорта ни один из городов не достижим из города отправления за данный лимит стоимости\n')
                print('С помощью данных видов транспорта ни один из городов не достижим из города отправления за данный лимит стоимости\n', file=log)
                stdscr.refresh()
            stdscr.addstr('Нажмите любую клавишу для перехода в меню\n')
            stdscr.refresh()
            curses.curs_set(0)
            stdscr.getch()

        elif current_item_index == LIMITTIME_MODE:
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
            stdscr.addstr('Введите лимит времени:\n')
            stdscr.refresh()
            curses.curs_set(1)
            limit_time_str = str(stdscr.getstr(), 'utf-8', errors='ignore')         
            while limit_time_str == '' or not limit_time_str.isdigit() or int(limit_time_str) <= 0:
                stdscr.clear()
                stdscr.addstr('Введите лимит времени:\n')
                stdscr.refresh()
                curses.curs_set(1)
                limit_time_str = str(stdscr.getstr(), 'utf-8', errors='ignore')      
            print(f'Лимит времени: {limit_time_str}', file=log)
            limit_time = int(limit_time_str)
            from_id = station_name_to_id[station_from]

            start_operation = time()

            d, p = dijkstra(from_id, next_station_id, graph, 0, vehicles_types)

            trips_map = {}
            for i in range(next_station_id):
                if i != from_id and d[i] <= limit_time:
                    trip = Trip()
                    current_station = i
                    while current_station != from_id:
                        next_cruise = p[current_station]
                        trip += next_cruise
                        current_station = next_cruise.from_id
                    trips_map[i] = trip
            end_operation = time()
            print(f'Время выполнения запроса: {end_operation - start_operation} сек.', file=log)

            print(f'Max RSS: {getrusage(RUSAGE_SELF).ru_maxrss} KiB\n', file=log)

            if len(trips_map) > 0:
                for station_from_id, trip in trips_map.items():
                    station_from = station_id_to_name[station_from_id]

                    stdscr.addstr(f'До станции "{station_from}":\n')
                    stdscr.refresh()
                    print(f'До станции "{station_from}":', file=log)

                    for count in range(1, trip.cruises_num + 1):
                        cruise = trip[count - 1]
                        from_st = station_id_to_name[cruise.from_id]
                        to_st = station_id_to_name[cruise.to_id]
                        vehicle = vehicle_id_to_name[cruise.vehicle_id]
                        time_ = cruise.cruise_time
                        cost_ = cruise.cruise_cost
                        stdscr.addstr(f'{count}) Из: {from_st}, в: {to_st}, транспорт: {vehicle}, время: {time_}, стоимость: {cost_}\n')
                        stdscr.refresh()
                        print(f'{count}) Из: {from_st}, в: {to_st}, транспорт: {vehicle}, время: {time_}, стоимость: {cost_}', file=log)
                    stdscr.addstr(f'Время пути: {trip.trip_time}\n')
                    stdscr.refresh()
                    print(f'Время пути: {trip.trip_time}', file=log)
                    stdscr.addstr(f'Стоимость пути: {trip.trip_cost}\n')
                    stdscr.refresh()
                    print(f'Стоимость пути: {trip.trip_cost}', file=log)
                print(file=log)
            else:
                stdscr.addstr('С помощью данных видов транспорта ни один из городов не достижим из города отправления за данный лимит времени\n')
                print('С помощью данных видов транспорта ни один из городов не достижим из города отправления за данный лимит времени\n', file=log)
                stdscr.refresh()
            stdscr.addstr('Нажмите любую клавишу для перехода в меню\n')
            stdscr.refresh()
            curses.curs_set(0)
            stdscr.getch()

        elif current_item_index == WANT_TO_EXIT:
            want_to_exit = True

    curses.endwin()

    end_program = time()
    print(f'Время выполнения программы: {end_program - start_program} сек.', file=log)

    print(f'Max RSS: {getrusage(RUSAGE_SELF).ru_maxrss} KiB\n', file=log)

    log.close()


if __name__ == '__main__':
    curses.wrapper(main)