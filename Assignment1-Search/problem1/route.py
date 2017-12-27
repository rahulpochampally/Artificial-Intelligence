
'''

1)Which search algorithm seems to work best for each routing options?
--- Astar algorithm works better in terms of distance and time, which are much lower than other algorithms

2)Which algorithm is fastest in terms of the amount of computation time required by your program, and by how much, according to your experiments?
    Experiment 1 - Bloomington,_Indiana Chicago,_Illinois
                A* takes 0.379s
                BFS takes 0.566s
                DFS takes 11.042s
                Uniform Segements 3.171s
                Uniform Time 1.777s
                Uniform Distance 2.553s
    Experiment 2 - Bloomington,_Indiana New_York,_New_York
                A* takes 3.685s
                BFS takes 5.047s
                DFS takes 1.535s
                Uniform Segements 64m13.019s
                Uniform Time 3m50.747s
                Uniform Distance 5.145s
    As seen in the experiment BFS takes less time but it does not see for the shortest distance from point to point which makes A* more accurate even though the time is higher

3)Which algorithm requires the least memory, and by how much, according to your experiments?
    A* and DFS compete in this criteria which takes less memory. A* channels the path towards its goal so it takes takes the least memory.
    On the other side DFS goes along one path to child node and traces back to root to tranverse other side

4)Which heuristic function(s) did you use, how good is it, and how might you make it/them better?
    h(s) = d(s)+h'(s)
    d(s) -- distance travelled from start city to imtermediate city
    h'(s)-- distance from the intermediate city to goal city
    By this, the algorithm channels the path to have the shortest distance towards the goal
    In experiment 1 - Bloomington,_Indiana Chicago,_Illinois A* Algorithm gives 262 miles whereas Google Maps gives 232 miles
    In experiment 2 - Bloomington,_Indiana New_York,_New_York A8 Algorithm gives 821 miles whereas Google Maps gives 790 miles
    There is almost a 30 mile difference (which may increase for farther cities)
'''


import sys
import re

from math import radians, sin, cos, sqrt, atan2

list_city = []
list_lat = []
list_lon = []
list_city1 = []
list_city2 = []
miles = []
speed = []
highway = []

with open('city-gps.txt', 'r') as f:
    for line in f:
        list_line = re.findall(r"[\S']+", line)
        # list_city.append(list_line[0])
        list_lat.append(float(list_line[1]))
        list_lon.append(float(list_line[2]))
with open('city-gps.txt', 'r') as f:
    for line in f:
        list_line = re.findall(r"[\w,\w+']+", line)
        list_city.append(list_line[0])
with open('road-segments.txt', 'r') as f:
    for line in f:
        list_line = re.findall(r"[\S']+", line)
        list_city1.append(list_line[0])
        list_city2.append(list_line[1])
        miles.append(int(list_line[2]))
        speed.append(int(list_line[3]))
        highway.append((list_line[4]))

for n, i in enumerate(speed):
    if i == 0:
        speed[n] = 45


def successor(city):
    succ_city = []
    indices1 = [i for i, x in enumerate(list_city1) if x == city]
    indices2 = [i for i, x in enumerate(list_city2) if x == city]
    for x in range(len(indices1)):
        succ_city.append(list_city2[indices1[x]])
    for x in range(len(indices2)):
        succ_city.append(list_city1[indices2[x]])
    # return_val = list(set(succ_city))
    for s in succ_city:
        for q in traversed_city:
            if s == q:
                succ_city = [p for p in succ_city if p != s]
    for s in succ_city:
        for q in fringe:
            if s == q:
                succ_city = [p for p in succ_city if p != s]
    succ_map[city] = succ_city
    return succ_city


def is_goal(city):
    if (city == end_city):
        return True


def DFS(start_city, end_city, cost_function):
    while (len(fringe) > 0):
        current_city = fringe.pop()
        traversed_city.append(current_city)

        succ = successor(current_city)
        for s in succ:
            if is_goal(s):
                return s
            fringe.append(s)
    return False


def BFS(start_city, end_city, cost_function):
    while (len(fringe) > 0):
        current_city = fringe.pop(0)
        traversed_city.append(current_city)

        succ = successor(current_city)
        for s in succ:
            if is_goal(s):
                return s
            fringe.append(s)
    return False


def uniformSuccessor(city):
    succ_city = []
    path_city = []
    current = city[1][-1]
    indices1 = [i for i, x in enumerate(list_city1) if x == current]
    indices2 = [i for i, x in enumerate(list_city2) if x == current]
    for x in range(len(indices1)):
        path_city = []
        for i in city[1]:
            path_city.append(i)
        path_city.append(list_city2[indices1[x]])
        succ_city.append((city[0] + miles[indices1[x]], path_city,city[2]+miles[indices1[x]]/float(speed[indices1[x]])))
    for x in range(len(indices2)):
        path_city = []
        for i in city[1]:
            path_city.append(i)
        path_city.append(list_city1[indices2[x]])
        succ_city.append((city[0] + miles[indices2[x]], path_city,city[2]+miles[indices2[x]]/float(speed[indices2[x]])))

    for s in succ_city:
        a = s[1][-1]
        for p in traversed_city:
            if a==p:
                 succ_city = [q for q in succ_city if q != s]
    return succ_city


def uniformSuccessor_time(city):
    succ_city = []
    path_city = []
    current = city[1][-1]
    indices1 = [i for i, x in enumerate(list_city1) if x == current]
    indices2 = [i for i, x in enumerate(list_city2) if x == current]
    for x in range(len(indices1)):
        path_city = []
        for i in city[1]:
            path_city.append(i)
        path_city.append(list_city2[indices1[x]])
        succ_city.append((city[0] + miles[indices1[x]]/float(speed[indices1[x]]), path_city,city[2]+miles[indices1[x]]))
    for x in range(len(indices2)):
        path_city = []
        for i in city[1]:
            path_city.append(i)
        path_city.append(list_city1[indices2[x]])
        succ_city.append((city[0] + miles[indices2[x]]/float(speed[indices2[x]]), path_city,city[2]+miles[indices2[x]]))

    for s in succ_city:
        a = s[1][-1]
        for p in traversed_city:
            if a==p:
                 succ_city = [q for q in succ_city if q != s]
    return succ_city

def uniformSuccessor_distance(city):
    succ_city = []
    path_city = []
    current = city[1][-1]
    indices1 = [i for i, x in enumerate(list_city1) if x == current]
    indices2 = [i for i, x in enumerate(list_city2) if x == current]
    for x in range(len(indices1)):
        path_city = []
        for i in city[1]:
            path_city.append(i)
        path_city.append(list_city2[indices1[x]])
        town1 = current;
        town2 = list_city2[indices1[x]]
        x1 = 39.8283
        x2 = 98.5795
        y1 = 39.8283
        y2 = 98.5795
        for xx in list_city:
            if xx == town1:
                x1=float(list_lat[list_city.index(xx)])
                y1=float(list_lon[list_city.index(xx)])
            if xx == town2:
                x2 = float(list_lat[list_city.index(xx)])
                y2 = float(list_lon[list_city.index(xx)])
        lat1 = radians(x1)
        lon1 = radians(y1)
        lat2 = radians(x2)
        lon2 = radians(y2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = 6373 * c
        if x2 == 0:
            distance = city[2]+miles[indices1[x]]
        succ_city.append((distance, path_city,city[2]+miles[indices1[x]],city[3]+miles[indices1[x]]/float(speed[indices1[x]])))
    for x in range(len(indices2)):
        path_city = []
        for i in city[1]:
            path_city.append(i)
        path_city.append(list_city1[indices2[x]])
        town1 = current;
        town2 = list_city2[indices2[x]]
        x1 = 39.8283
        x2 = 98.5795
        y1 = 39.8283
        y2 = 98.5795
        for xx in list_city:
            if xx == town1:
                x1 = float(list_lat[list_city.index(xx)])
                y1 = float(list_lon[list_city.index(xx)])
            if xx == town2:
                x2 = float(list_lat[list_city.index(xx)])
                y2 = float(list_lon[list_city.index(xx)])
        lat1 = radians(x1)
        lon1 = radians(y1)
        lat2 = radians(x2)
        lon2 = radians(y2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = 6373 * c
        if x2 == 0:
            distance = city[2]+miles[indices2[x]]
        succ_city.append((distance, path_city,city[2]+miles[indices2[x]],city[3]+miles[indices2[x]]/float(speed[indices2[x]])))
    for s in succ_city:
        a = s[1][-1]
        for p in traversed_city:
            if a==p:
                 succ_city = [q for q in succ_city if q != s]
    return succ_city

def UniformCostSearch():
    while (len(UniformFringe) > 0):
        currentCity = UniformFringe.pop()
        traversed_city.append(currentCity[1][-1])
        path_map.append(currentCity)
        if cost_func == "segments":
            succ = uniformSuccessor(currentCity)
        elif cost_func == "time":
            succ = uniformSuccessor_time(currentCity)
        elif cost_func == "distance":
            succ = uniformSuccessor_distance(currentCity)
        for s in succ:
            if is_goal(s[1][-1]):
                return s
            UniformFringe.append(s)
        UniformFringe.sort(reverse=True)
    return False

def astarSuccessor(city):
    succ_city = []
    path_city = []
    current = city[1][-1]
    indices1 = [i for i, x in enumerate(list_city1) if x == current]
    indices2 = [i for i, x in enumerate(list_city2) if x == current]
    for x in range(len(indices1)):
        path_city = []
        for i in city[1]:
            path_city.append(i)
        path_city.append(list_city2[indices1[x]])
        town1 = end_city;
        town2 = list_city2[indices1[x]]
        x1 = 0
        x2 = 0
        y1 = 0
        y2 = 0
        for xx in list_city:
            if xx == town1:
                x1 = float(list_lat[list_city.index(xx)])
                y1 = float(list_lon[list_city.index(xx)])
            if xx == town2:
                x2 = float(list_lat[list_city.index(xx)])
                y2 = float(list_lon[list_city.index(xx)])

        lat1 = radians(x1)
        lon1 = radians(y1)
        lat2 = radians(x2)
        lon2 = radians(y2)

        dlon = lon2-lon1
        dlat = lat2-lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = 6373*c
        if x2==0:
            distance = city[0] + 1.6*miles[indices1[x]]


        succ_city.append((1.6*city[4]+ 1.6*miles[indices1[x]]+distance, path_city, city[2] + miles[indices1[x]],
                          city[3] +miles[indices1[x]] / float(speed[indices1[x]]),city[4] + miles[indices1[x]]))
    for x in range(len(indices2)):
        path_city = []
        for i in city[1]:
            path_city.append(i)
        path_city.append(list_city1[indices2[x]])
        town1 = end_city;
        town2 = list_city2[indices2[x]]
        x1 = 39.8283
        x2 = 98.5795
        y1 = 39.8283
        y2 = 98.5795
        for xx in list_city:
            if xx == town1:
                x1 = float(list_lat[list_city.index(xx)])
                y1 = float(list_lon[list_city.index(xx)])
            if xx == town2:
                x2 = float(list_lat[list_city.index(xx)])
                y2 = float(list_lon[list_city.index(xx)])

        lat1 = radians(x1)
        lon1 = radians(y1)
        lat2 = radians(x2)
        lon2 = radians(y2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = 6373 * c
        if x2==0:
            distance = city[0] + 1.6 * miles[indices2[x]]
        succ_city.append((1.6*city[4]+1.6*miles[indices2[x]]+ distance, path_city, city[2] + miles[indices2[x]],
                         city[3] + miles[indices2[x]] / float(speed[indices2[x]]),city[4] + miles[indices2[x]]))
    for s in succ_city:
        a = s[1][-1]
        for p in traversed_city:
            if a == p:
                succ_city = [q for q in succ_city if q != s]
    return succ_city


def astarSearch():
    while (len(astarFringe)>0):
        currentCity = astarFringe.pop()
        traversed_city.append(currentCity[1][-1])
        path_map.append(currentCity)
        succ = astarSuccessor(currentCity)
        for s in succ:
            if is_goal(s[1][-1]):
                return s
            astarFringe.append(s)
        astarFringe.sort(reverse=True)
    return False



traversed_city = []
start_city = str(sys.argv[1])
end_city = (sys.argv[2])
route_algo = (sys.argv[3])
cost_func = (sys.argv[4])
fringe = [start_city]
UniformFringe = []
UniformFringe.append((0,fringe,0,0))
astarFringe = []
astarFringe.append((0,fringe,0,0,0))
path = []
succ_map = {}
path_map = []

def calculate_distance(path):
    distance = 0
    time = 0
    for i in range(len(path) - 1):
        if (path[i] in list_city1 and path[i + 1] in list_city2) or (
                path[i] in list_city2 and path[i + 1] in list_city1):
            indices1 = [j for j, x in enumerate(list_city1) if x == path[i]]
            indices2 = [j for j, x in enumerate(list_city2) if x == path[i + 1]]
            indices3 = [j for j, x in enumerate(list_city1) if x == path[i + 1]]
            indices4 = [j for j, x in enumerate(list_city2) if x == path[i]]
            common_index1 = list(set(indices1) & set(indices2))
            common_index2 = list(set(indices3) & set(indices4))
            if len(common_index1) != 0:
                distance = distance + miles[common_index1[0]]
                time = time + miles[common_index1[0]] / float(speed[common_index1[0]])
            elif len(common_index2) != 0:
                distance = distance + miles[common_index2[0]]
                time = time + miles[common_index2[0]] / float(speed[common_index2[0]])
    return str(distance) + " " + str(format(time,'.4f'))

def print_path(city):
    path.append(city)
    while (city != start_city):
        for parent_map in succ_map.keys():
            traversed_map = succ_map[parent_map]
            if city in traversed_map:
                path.append(parent_map)
                break
        city = parent_map
    path.reverse()
    print calculate_distance(path)+" "+" ".join(path)

if route_algo == "dfs":
    DFS(start_city, end_city, cost_func)
    print_path(end_city)
elif route_algo == "bfs":
    BFS(start_city, end_city, cost_func)
    print_path(end_city)
elif route_algo == "uniform":
    if cost_func == "segments":
        print_text = UniformCostSearch()
        print str(print_text[0])+" "+str(format(print_text[2],'.4f'))+" "+" ".join(print_text[1])
    elif cost_func == "time":
        print_text = UniformCostSearch()
        print str(print_text[2])+" "+str(format(print_text[0],'.4f'))+" "+" ".join(print_text[1])
    elif cost_func == "distance":
        print_text = UniformCostSearch()
        print str(print_text[2])+" "+ str(format(print_text[3],'.4f'))+" "+" ".join(print_text[1])
elif route_algo == "astar":
    print_text = astarSearch()
    print str(print_text[2])+" "+str(format(print_text[3],'.4f'))+" "+" ".join(print_text[1])
else:print "Please enter correct routing options"



