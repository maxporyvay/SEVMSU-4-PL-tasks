from task_graphs_py.classes import INF, Queue, MinHeap


def bfs(s, n, graph, vehicles_types):
    d = [INF] * n
    p = [INF] * n

    q = Queue(INF)
    q.push(s)
    
    d[s] = 0
    
    while q.size() > 0:
        v = q.pop()
        for u, cruises in graph.getCruisesMapFromStation(v):
            flag = False
            best_cruise = -1
            for cruise in cruises:
                if cruise.vehicle_id in vehicles_types:
                    flag = True
                    best_cruise = cruise
            if flag and d[u] == INF:
                q.push(u)
                d[u] = d[v] + 1
                p[u] = best_cruise

    return d, p


def dijkstra(s, n, graph, to_optimize, vehicles_types):
    d = [INF] * n
    p = [INF] * n

    q = MinHeap()
    q.insert((0, s))

    d[s] = 0

    while q.size() > 0:
        cur_d, v = q.extract()
        if cur_d > d[v]:
            continue
        for u, cruises in graph.getCruisesMapFromStation(v):
            min_w = INF
            cruise_for_min_w = -1
            for cruise in cruises:
                w = -1
                if to_optimize == 0:
                    w = cruise.cruise_time
                elif to_optimize == 1:
                    w = cruise.cruise_cost
                if cruise.vehicle_id in vehicles_types and w < min_w:
                    min_w = w
                    cruise_for_min_w = cruise
            if min_w < INF and d[u] > d[v] + min_w:
                d[u] = d[v] + min_w
                p[u] = cruise_for_min_w
                q.insert((d[u], u))

    return d, p


def dijkstra_extra_cond(s, n, graph, to_optimize, vehicles_types):
    d = [INF] * n
    extra = [INF] * n
    p = [INF] * n

    q = MinHeap()
    q.push((0, 0, s))

    d[s] = 0
    extra[s] = 0
    
    while q.size() > 0:
        cur_d, _, v = q.extract()
        if cur_d > d[v]:
            continue
        for u, cruises in graph.getCruisesMapFromStation(v):
            min_w = INF
            extra_for_min_w = INF
            cruise_for_min_w = -1
            for cruise in cruises:
                w = -1
                extra = -1
                if to_optimize == 0:
                    w = cruise.cruise_time
                    extra = cruise.cruise_cost
                elif to_optimize == 1:
                    w = cruise.cruise_cost
                    extra = cruise.cruise_time
                if cruise.vehicle_id in vehicles_types:
                    if w < min_w or w == min_w and extra < extra_for_min_w:
                        min_w = w
                        extra_for_min_w = extra
                        cruise_for_min_w = cruise
            if min_w < INF and (d[u] > d[v] + min_w or d[u] == d[v] + min_w and extra[u] > extra[v] + extra_for_min_w):
                d[u] = d[v] + min_w
                extra[u] = extra[v] + extra_for_min_w
                p[u] = cruise_for_min_w
                q.push((d[u], extra[u], u))
    
    return d, extra, p