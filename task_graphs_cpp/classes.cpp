#include "classes.h"

Cruise::Cruise()
{

};

Cruise::Cruise(uint32_t f_id, uint32_t t_id, uint32_t v_id, uint32_t t, uint32_t c)
{
    from_id = f_id;
    to_id = t_id;
    vehicle_id = v_id;
    cruise_time = t;
    cruise_cost = c;
}

Cruise::Cruise(const Cruise &cruise)
{
    from_id = cruise.from_id;
    to_id = cruise.to_id;
    vehicle_id = cruise.vehicle_id;
    cruise_time = cruise.cruise_time;
    cruise_cost = cruise.cruise_cost;
}

Trip::Trip()
{
    cruises_num = 0;
}

Trip Trip::operator+(Cruise &cruise)
{
    cruises_vector.push_back(cruise);
    cruises_num++;
    return *this;
}

Trip Trip::operator+=(Cruise &cruise)
{
    return *this + cruise;
}

Cruise& Trip::operator[](uint32_t index)
{
    return cruises_vector[cruises_num - index - 1];
}