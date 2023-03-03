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

pair<vector<uint32_t>, vector<Cruise>> bfs(uint32_t s, uint32_t n, map<uint32_t, map<uint32_t, vector<Cruise*>>> graph, unordered_set<uint32_t> vehicles_types)
{
    queue<uint32_t> q;
    q.push(s);
    
    vector<uint32_t> d(n, INF);
    vector<Cruise> p(n);
    d[s] = 0;
    
    while (!q.empty()) {
        uint32_t v = q.front();
        q.pop();
        for (pair<uint32_t, vector<Cruise*>> in_map : graph[v]) {
            uint32_t u = in_map.first;
            vector<Cruise*> cruises = in_map.second;
            bool flag = false;
            Cruise best_cruise;
            for (Cruise* cruise : cruises)
            {
                if (vehicles_types.find(cruise->vehicle_id) != vehicles_types.end())
                {
                    flag = true;
                    best_cruise = *cruise;
                }
            }
            if (flag && d[u] == INF) {
                q.push(u);
                d[u] = d[v] + 1;
                p[u] = best_cruise;
            }
        }
    }

    return {d, p};
};

pair<vector<uint32_t>, vector<Cruise>> dijkstra(uint32_t s, uint32_t n, map<uint32_t, map<uint32_t, vector<Cruise*>>> graph, uint32_t to_optimize, unordered_set<uint32_t> vehicles_types)
{
    vector<uint32_t> d(n, INF);
    vector<Cruise> p(n);
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
            Cruise cruise_for_min_w;
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
                    cruise_for_min_w = *cruise;
                }
            }
            if (min_w < INF && d[u] > d[v] + min_w)
            {
                d[u] = d[v] + min_w;
                p[u] = cruise_for_min_w;
                q.push({d[u], u});
            }
        }
    }
    return {d, p};
}

tuple<vector<uint32_t>, vector<uint32_t>, vector<Cruise>> dijkstra_extra_cond(uint32_t s, uint32_t n, map<uint32_t, map<uint32_t, vector<Cruise*>>> graph, uint32_t to_optimize, unordered_set<uint32_t> vehicles_types)
{
    vector<uint32_t> d(n, INF);
    vector<uint32_t> extra(n, INF);
    vector<Cruise> p(n);
    d[s] = 0;
    extra[s] = 0;
    priority_queue<Triad, vector<Triad>, greater<Triad>> q;
    q.push({0, 0, s});
    while (!q.empty())
    {
        Triad top_triad = q.top();
        uint32_t cur_d = get<0>(top_triad);
        uint32_t v = get<2>(top_triad);
        q.pop();
        if (cur_d > d[v])
            continue;
        for (pair<uint32_t, vector<Cruise*>> in_map : graph[v])
        {
            uint32_t u = in_map.first;
            vector<Cruise*> cruises = in_map.second;
            uint32_t min_w = INF;
            uint32_t extra_for_min_w = INF;
            Cruise cruise_for_min_w;
            for (Cruise* cruise : cruises)
            {
                uint32_t w, extra;
                if (to_optimize == 0)
                {
                    w = cruise->cruise_time;
                    extra = cruise->cruise_cost;
                }
                else if (to_optimize == 1)
                {
                    w = cruise->cruise_cost;
                    extra = cruise->cruise_time;
                }
                if (vehicles_types.find(cruise->vehicle_id) != vehicles_types.end())
                {
                    if (w < min_w || w == min_w && extra < extra_for_min_w)
                    {
                        min_w = w;
                        extra_for_min_w = extra;
                        cruise_for_min_w = *cruise;
                    }
                }
            }
            if (min_w < INF && (d[u] > d[v] + min_w || d[u] == d[v] + min_w && extra[u] > extra[v] + extra_for_min_w))
            {
                d[u] = d[v] + min_w;
                extra[u] = extra[v] + extra_for_min_w;
                p[u] = cruise_for_min_w;
                q.push({d[u], extra[u], u});
            }
        }
    }
    return {d, extra, p};
}

#endif