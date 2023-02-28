#ifndef ALGORITHMS_H
#define ALGORITHMS_H

#include "classes.h"

#include <vector>
#include <queue>
#include <map>
#include <unordered_set>
#include <utility>
#include <stdint.h>
#include <iostream>

using namespace std;

typedef pair<uint32_t, uint32_t> Pair;

const uint32_t INF = UINT32_MAX;

void bfs()
{

};

pair<vector<uint32_t>, vector<uint32_t>> dijkstra(uint32_t s, uint32_t n, map<uint32_t, map<uint32_t, vector<Cruise*>>> graph, uint32_t to_optimize, unordered_set<uint32_t> vehicles_types)
{
    vector<uint32_t> d(n, INF);
    vector<uint32_t> p(n, INF);
    d[s] = 0;
    priority_queue<Pair, vector<Pair>, greater<Pair>> q;
    q.push({0, s});
    while (!q.empty())
    {
        Pair top_pair = q.top();
        uint32_t cur_d = top_pair.first;
        uint32_t v = top_pair.second;
        q.pop();
        if (cur_d > d[v])
            continue;
        for (pair<uint32_t, vector<Cruise*>> in_map : graph[v])
        {
            uint32_t u = in_map.first;
            vector<Cruise*> cruises = in_map.second;
            uint32_t min_w = INF;
            for (Cruise* cruise : cruises)
            {
                uint32_t w;
                if (to_optimize == 0)
                {
                    w = cruise->cruise_time;
                }
                else if (to_optimize == 1)
                {
                    w = cruise->cruise_cost;
                }
                if (vehicles_types.find(cruise->vehicle_id) != vehicles_types.end() && w < min_w)
                {
                    min_w = w;
                }
            }
            if (min_w < INF && d[u] > d[v] + min_w)
            {
                d[u] = d[v] + min_w;
                p[u] = v;
                q.push({d[u], u});
            }
        }
    }
    return {d, p};
}

#endif