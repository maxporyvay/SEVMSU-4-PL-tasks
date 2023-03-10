#ifndef ALGORITHMS_H
#define ALGORITHMS_H

#include "classes.hpp"

const uint32_t INF = UINT32_MAX;

void bfs(uint32_t s,
         CruisesGraph graph,
         std::unordered_set<uint32_t> vehicles_types,
         std::vector<uint32_t> &d,
         std::vector<Cruise> &p);

void dijkstra(uint32_t s,
              CruisesGraph graph,
              uint32_t to_optimize,
              std::unordered_set<uint32_t> vehicles_types,
              std::vector<uint32_t> &d,
              std::vector<Cruise> &p);

void dijkstra_extra_cond(uint32_t s,
                         CruisesGraph graph,
                         uint32_t to_optimize,
                         std::unordered_set<uint32_t> vehicles_types,
                         std::vector<uint32_t> &d,
                         std::vector<uint32_t> &extra,
                         std::vector<Cruise> &p);

#endif