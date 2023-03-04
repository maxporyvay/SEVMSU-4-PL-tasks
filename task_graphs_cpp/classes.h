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

    Cruise();

    Cruise(uint32_t f_id, uint32_t t_id, uint32_t v_id, uint32_t t, uint32_t c);

    Cruise(const Cruise &cruise);
};

struct Trip
{
    vector<Cruise> cruises_vector;

    uint32_t cruises_num;

    Trip();

    Trip operator+(Cruise &cruise);

    Trip operator+=(Cruise &cruise);

    Cruise& operator[](uint32_t index);
};

#endif