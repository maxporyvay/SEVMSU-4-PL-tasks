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

    Cruise()
    {

    };

    Cruise(uint32_t f_id, uint32_t t_id, uint32_t v_id, uint32_t t, uint32_t c)
    {
        from_id = f_id;
        to_id = t_id;
        vehicle_id = v_id;
        cruise_time = t;
        cruise_cost = c;
    }

    Cruise(const Cruise &cruise)
    {
        from_id = cruise.from_id;
        to_id = cruise.to_id;
        vehicle_id = cruise.vehicle_id;
        cruise_time = cruise.cruise_time;
        cruise_cost = cruise.cruise_cost;
    }
};

struct Trip
{
    stack<Cruise> cruises_stack;

    Trip operator+(Cruise &cruise)
    {
        cruises_stack.push(cruise);
        return *this;
    }

    Trip operator+=(Cruise &cruise)
    {
        return *this + cruise;
    }

    // Cruise& operator[](uint32_t index)
    // {

    // };

    Cruise next()
    {
        Cruise top = cruises_stack.top();
        cruises_stack.pop();
        return top;
    }

    bool finished()
    {
        return cruises_stack.empty();
    }
};

#endif