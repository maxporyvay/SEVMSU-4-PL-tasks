#ifndef CLASSES_H
#define CLASSES_H

#include <stdint.h>
#include <vector>
#include <queue>
#include <map>
#include <unordered_set>
#include <utility>
#include <tuple>

struct Cruise
{
    uint32_t from_id;
    uint32_t to_id;
    uint32_t vehicle_id;
    uint32_t cruise_time;
    uint32_t cruise_cost;

    Cruise();

    Cruise(uint32_t f_id, uint32_t t_id, uint32_t v_id, uint32_t t, uint32_t c);
};

struct Trip
{
    std::vector<Cruise> cruises_vector;

    uint32_t cruises_num;

    Trip();

    Trip operator+(Cruise &cruise);

    Trip operator+=(Cruise &cruise);

    Cruise& operator[](uint32_t index);
};

struct CruisesGraph
{
    std::map<uint32_t, std::map<uint32_t, std::vector<Cruise>>> graph;

    void insertCruise(Cruise &cruise);

    std::map<uint32_t, std::vector<Cruise>> getCruisesMapFromStation(uint32_t station_id);
};

typedef std::pair<uint32_t, uint32_t> TwoInts;

typedef std::tuple<uint32_t, uint32_t, uint32_t> ThreeInts;

#endif