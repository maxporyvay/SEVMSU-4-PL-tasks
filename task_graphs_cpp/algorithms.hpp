#ifndef ALGORITHMS_H
#define ALGORITHMS_H

#include "classes.hpp"

const uint32_t INF = UINT32_MAX;

std::pair<std::vector<uint32_t>, std::vector<Cruise>> bfs(uint32_t s, uint32_t n, CruisesGraph graph, std::unordered_set<uint32_t> vehicles_types);

std::pair<std::vector<uint32_t>, std::vector<Cruise>> dijkstra(uint32_t s, uint32_t n, CruisesGraph graph, uint32_t to_optimize, std::unordered_set<uint32_t> vehicles_types);

std::tuple<std::vector<uint32_t>, std::vector<uint32_t>, std::vector<Cruise>> dijkstra_extra_cond(uint32_t s, uint32_t n, CruisesGraph graph, uint32_t to_optimize, std::unordered_set<uint32_t> vehicles_types);

#endif