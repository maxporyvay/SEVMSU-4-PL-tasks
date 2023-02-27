#ifndef ALGORITHMS_H
#define ALGORITHMS_H

#include "classes.h"

#include <vector>
#include <queue>
#include <map>
#include <unordered_set>
#include <utility>

using namespace std;

typedef pair<int, int> Pair;

// const uint INF = 4294967295;
const int INF = 100000;

void bfs()
{

};

pair<vector<int>, vector<int>> dijkstra(int s, int n, map<int, map<int, vector<Cruise*>>> graph, int to_optimize, unordered_set<int> vehicles_types)
{
    vector<int> d(n, INF);
    vector<int> p(n, INF);
    d[s] = 0;
    priority_queue<Pair, vector<Pair>, greater<Pair>> q;
    q.push({0, s});
    while (!q.empty())
    {
        auto top_pair = q.top();
        int cur_d = top_pair.first;
        int v = top_pair.second;
        q.pop();
        if (cur_d > d[v])
            continue;
        for (auto in_map : graph[v])
        {
            int u = in_map.first;
            vector<Cruise*> cruises = in_map.second;
            int min_w = INF;
            for (auto cruise : cruises)
            {
                int w;
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
            if (d[u] > d[v] + min_w)
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