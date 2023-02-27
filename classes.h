#ifndef CLASSES_H
#define CLASSES_H

#include <vector>

using namespace std;

struct Cruise
{
    int from_id;
    int to_id;
    int vehicle_id;
    int cruise_time;
    int cruise_cost;

    Cruise(int f_id, int t_id, int v_id, int t, int c)
    {
        from_id = f_id;
        to_id = t_id;
        vehicle_id = v_id;
        cruise_time = t;
        cruise_cost = c;
    }
};

struct InversedTrip
{
    vector<int> stations_list;
    int trip_time;
    int trip_cost;
    int stations_num;

    InversedTrip()
    {
        trip_time = 0;
        trip_cost = 0;
        stations_num = 0;
    }

    InversedTrip(const Cruise& cruise)
    {
        stations_list = {cruise.to_id, cruise.from_id};
        trip_time = cruise.cruise_time;
        trip_cost = cruise.cruise_cost;
        stations_num = 2;
    }

    InversedTrip& operator+=(const InversedTrip& x)
    {
        for (int i = 0; i < x.stations_num; i++)
        {
            stations_list.push_back(x.stations_list[i]);
        }
        stations_num += x.stations_num;
        trip_time += x.trip_time;
        trip_time += x.trip_cost;
        return *this;
    }

    int& operator[](int index)
    {
        return stations_list[stations_num - index - 1];
    }
};

#endif