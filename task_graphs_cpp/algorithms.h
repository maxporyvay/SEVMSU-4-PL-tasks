#ifndef ALGORITHMS_H
#define ALGORITHMS_H

#include "classes.h"

#include <vector>
#include <queue>
#include <map>
#include <unordered_set>
#include <utility>
#include <stdint.h>
#include <tuple>

using namespace std;

typedef pair<uint32_t, uint32_t> Pair;
typedef tuple<uint32_t, uint32_t, uint32_t> Triad;

const uint32_t INF = UINT32_MAX;

pair<vector<uint32_t>, vector<Cruise>> bfs(uint32_t s, uint32_t n, map<uint32_t, map<uint32_t, vector<Cruise*>>> graph, unordered_set<uint32_t> vehicles_types);

pair<vector<uint32_t>, vector<Cruise>> dijkstra(uint32_t s, uint32_t n, map<uint32_t, map<uint32_t, vector<Cruise*>>> graph, uint32_t to_optimize, unordered_set<uint32_t> vehicles_types);

tuple<vector<uint32_t>, vector<uint32_t>, vector<Cruise>> dijkstra_extra_cond(uint32_t s, uint32_t n, map<uint32_t, map<uint32_t, vector<Cruise*>>> graph, uint32_t to_optimize, unordered_set<uint32_t> vehicles_types);

#endif