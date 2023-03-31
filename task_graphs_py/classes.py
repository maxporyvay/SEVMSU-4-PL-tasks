INF = 2 ** 32 - 1 # 4294967295


class Queue:
    def __init__(self, maxsize):
        self.queue = [None] * maxsize
        self.maxsize = maxsize
        self.head = -1
        self.tail = -1

    def push(self, num):
        self.tail += 1
        self.queue[self.tail % self.maxsize] = num
        if self.head < 0:
            self.head = 0

    def pop(self):
        if self.head >= 0:
            if self.head >= self.tail:
                front = self.queue[self.head % self.maxsize]
                self.head = -1
                self.tail = -1
            else:
                front = self.queue[self.head % self.maxsize]
                self.head += 1
            return front

    def front(self):
        if self.head >= 0:
            return self.queue[self.head % self.maxsize]

    def size(self):
        if self.head >= 0:
            return self.tail - self.head + 1
        return 0

    def clear(self):
        self.head = -1
        self.tail = -1


class MinHeap:
    def __init__(self):
        self.heap = []

    def insert(self, num):
        self.heap.append(num)
        idx = len(self.heap) - 1
        while idx > 0 and self.heap[idx] < self.heap[(idx - 1) // 2]:
            self.heap[idx], self.heap[(idx - 1) // 2] = self.heap[(idx - 1) // 2], self.heap[idx]
            idx = (idx - 1) // 2

    def extract(self):
        ans = self.heap[0]
        self.heap[0] = self.heap[-1]
        idx = 0
        while 2 * idx + 2 < len(self.heap):
            min_son_idx = 2 * idx + 1
            if self.heap[min_son_idx] > self.heap[2 * idx + 2]:
                min_son_idx = 2 * idx + 2
            if self.heap[idx] > self.heap[min_son_idx]:
                self.heap[idx], self.heap[min_son_idx] = self.heap[min_son_idx], self.heap[idx]
                idx = min_son_idx
            else:
                break
        self.heap.pop()
        return ans


class Cruise:
    def __init__(self, f_id=-1, t_id=-1, v_id=-1, t=-1, c=-1)
        self.from_id = f_id
        self.to_id = t_id
        self.vehicle_id = v_id
        self.cruise_time = t
        self.cruise_cost = c


class Trip:
    def __init__(self):
        self.cruises_num = 0
        self.trip_cost = 0
        self.trip_time = 0
        self.cruises_vector = []

    def __add__(self, cruise):
        self.cruises_vector.append(cruise)
        self.cruises_num += 1
        self.trip_cost += cruise.cruise_cost
        self.trip_time += cruise.cruise_time
        return self

    def __iadd__(self, cruise):
        return self + cruise

    def __getitem__(self, index)
        return self.cruises_vector[self.cruises_num - index - 1]


class CruisesGraph:
    def __init__(self):
        self.graph = {}

    def insertCruise(cruise):
        if cruise.from_id not in self.graph:
            graph[cruise.from_id] = {cruise.to_id: [cruise]}
        elif cruise.to_id not in self.graph[cruise.from_id]:
            graph[cruise.from_id][cruise.to_id] = [cruise]
        else:
            graph[cruise.from_id][cruise.to_id].append(cruise)

    def getCruisesMapFromStation(station_id):
        return graph[station_id]