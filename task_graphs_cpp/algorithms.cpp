#include "algorithms.hpp"

BFS_Dijkstra_vectors_d_p bfs(uint32_t s, uint32_t n, CruisesGraph graph, std::unordered_set<uint32_t> vehicles_types)
{
    std::queue<uint32_t> q;
    q.push(s);
    
    std::vector<uint32_t> d(n, INF);
    std::vector<Cruise> p(n);
    d[s] = 0;
    
    while (!q.empty()) {
        uint32_t v = q.front();
        q.pop();
        for (auto cruises_map : graph.getCruisesMapFromStation(v)) {
            uint32_t u = cruises_map.first;
            std::vector<Cruise> cruises = cruises_map.second;
            bool flag = false;
            Cruise best_cruise;
            for (Cruise cruise : cruises)
            {
                if (vehicles_types.find(cruise.vehicle_id) != vehicles_types.end())
                {
                    flag = true;
                    best_cruise = cruise;
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

BFS_Dijkstra_vectors_d_p dijkstra(uint32_t s, uint32_t n, CruisesGraph graph, uint32_t to_optimize, std::unordered_set<uint32_t> vehicles_types)
{
    std::vector<uint32_t> d(n, INF);
    std::vector<Cruise> p(n);
    d[s] = 0;
    std::priority_queue<TwoInts, std::vector<TwoInts>, std::greater<TwoInts>> q;
    q.push({0, s});
    while (!q.empty())
    {
        TwoInts top_pair = q.top();
        uint32_t cur_d = top_pair.first;
        uint32_t v = top_pair.second;
        q.pop();
        if (cur_d > d[v])
            continue;
        for (auto cruises_map : graph.getCruisesMapFromStation(v))
        {
            uint32_t u = cruises_map.first;
            std::vector<Cruise> cruises = cruises_map.second;
            uint32_t min_w = INF;
            Cruise cruise_for_min_w;
            for (Cruise cruise : cruises)
            {
                uint32_t w;
                if (to_optimize == 0)
                {
                    w = cruise.cruise_time;
                }
                else if (to_optimize == 1)
                {
                    w = cruise.cruise_cost;
                }
                if (vehicles_types.find(cruise.vehicle_id) != vehicles_types.end() && w < min_w)
                {
                    min_w = w;
                    cruise_for_min_w = cruise;
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

Dijkstra_vectors_d_extra_p dijkstra_extra_cond(uint32_t s, uint32_t n, CruisesGraph graph, uint32_t to_optimize, std::unordered_set<uint32_t> vehicles_types)
{
    std::vector<uint32_t> d(n, INF);
    std::vector<uint32_t> extra(n, INF);
    std::vector<Cruise> p(n);
    d[s] = 0;
    extra[s] = 0;
    std::priority_queue<ThreeInts, std::vector<ThreeInts>, std::greater<ThreeInts>> q;
    q.push({0, 0, s});
    while (!q.empty())
    {
        ThreeInts top_triad = q.top();
        uint32_t cur_d = std::get<0>(top_triad);
        uint32_t v = std::get<2>(top_triad);
        q.pop();
        if (cur_d > d[v])
            continue;
        for (auto cruises_map : graph.getCruisesMapFromStation(v))
        {
            uint32_t u = cruises_map.first;
            std::vector<Cruise> cruises = cruises_map.second;
            uint32_t min_w = INF;
            uint32_t extra_for_min_w = INF;
            Cruise cruise_for_min_w;
            for (Cruise cruise : cruises)
            {
                uint32_t w, extra;
                if (to_optimize == 0)
                {
                    w = cruise.cruise_time;
                    extra = cruise.cruise_cost;
                }
                else if (to_optimize == 1)
                {
                    w = cruise.cruise_cost;
                    extra = cruise.cruise_time;
                }
                if (vehicles_types.find(cruise.vehicle_id) != vehicles_types.end())
                {
                    if (w < min_w || w == min_w && extra < extra_for_min_w)
                    {
                        min_w = w;
                        extra_for_min_w = extra;
                        cruise_for_min_w = cruise;
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