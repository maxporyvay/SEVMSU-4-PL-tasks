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
};

struct Trip
{
    std::vector<Cruise> cruises_vector;

    uint32_t cruises_num;

    uint32_t trip_cost;

    uint32_t trip_time;

    Trip::Trip()
    {
        cruises_num = 0;
        trip_cost = 0;
        trip_time = 0;
    }

    Trip Trip::operator+(Cruise &cruise)
    {
        cruises_vector.push_back(cruise);
        cruises_num++;
        trip_cost += cruise.cruise_cost;
        trip_time += cruise.cruise_time;
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
};

struct CruisesGraph
{
    std::map<uint32_t, std::map<uint32_t, std::vector<Cruise>>> graph;

    void CruisesGraph::insertCruise(Cruise &cruise)
    {
        if (graph.find(cruise.from_id) == graph.end())
        {
            std::map<uint32_t, std::vector<Cruise>> in_map;
            std::vector<Cruise> in_vec;
            in_vec.push_back(cruise);
            in_map[cruise.to_id] = in_vec;
            graph[cruise.from_id] = in_map;
        }
        else if (graph[cruise.from_id].find(cruise.to_id) == graph[cruise.from_id].end())
        {
            std::vector<Cruise> in_vec;
            in_vec.push_back(cruise);
            graph[cruise.from_id][cruise.to_id] = in_vec;
        }
        else
        {
            graph[cruise.from_id][cruise.to_id].push_back(cruise);
        }
    }

    std::map<uint32_t, std::vector<Cruise>> CruisesGraph::getCruisesMapFromStation(uint32_t station_id)
    {
        return graph[station_id];
    }
};

typedef std::pair<uint32_t, uint32_t> TwoInts;

typedef std::tuple<uint32_t, uint32_t, uint32_t> ThreeInts;

#endif