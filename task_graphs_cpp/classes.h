#ifndef CLASSES_H
#define CLASSES_H

#include <stack>
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
    stack<Cruise> cruises_stack;

    Trip operator+(Cruise &cruise);

    Trip operator+=(Cruise &cruise);

    // Cruise& operator[](uint32_t index);

    Cruise next();

    bool finished();
};

#endif