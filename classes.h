#ifndef CLASSES_H
#define CLASSES_H

#include <vector>
#include <stdint.h>

using namespace std;

struct Cruise
{
    uint32_t from_id;
    uint32_t to_id;
    uint32_t vehicle_id;
    uint32_t cruise_time;
    uint32_t cruise_cost;

    Cruise(uint32_t f_id, uint32_t t_id, uint32_t v_id, uint32_t t, uint32_t c)
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
    vector<uint32_t> stations_list;
    uint32_t trip_time;
    uint32_t trip_cost;
    uint32_t stations_num;

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
        for (uint32_t i = 0; i < x.stations_num; i++)
        {
            stations_list.push_back(x.stations_list[i]);
        }
        stations_num += x.stations_num;
        trip_time += x.trip_time;
        trip_time += x.trip_cost;
        return *this;
    }

    uint32_t& operator[](uint32_t index)
    {
        return stations_list[stations_num - index - 1];
    }
};

#endif