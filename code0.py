import sys
import json
import numpy as np
import networkx as nx
import itertools


with open("level0.json","r") as file:
    Data = json.load(file)

no_of_neighbours = Data['n_neighbourhoods']
no_of_restaurents = Data['n_restaurants']
neighbourhood = Data['neighbourhoods']

graph = {}
for i in range(0,no_of_neighbours):
    s1='n'
    s1 = s1+str(i)
    nestDict = neighbourhood[s1]
    del nestDict['order_quantity']
    graph[s1] = nestDict['distances']

graph1 = {}
restaurentData = Data['restaurants']

for i in range(0,no_of_restaurents):
    s2 = 'r'
    s2 = s2 + str(i)
    datas = restaurentData[s2]['neighbourhood_distance']
    datas1 = restaurentData[s2]['restaurant_distance']
    datas.append(0)
    graph1[s2] = datas
'''
for i in range(0,no_of_neighbours):
    s1='n'
    s1 = s1+str(i)
    data2 = graph1['r0']
    graph[s1].append(data2[i])

graph['r0'] = graph1['r0']
'''
#print(graph)
#print()

listValues = []
listNeighbours = []
'''
for i in range(0,no_of_neighbours+1):
    if i==(no_of_neighbours):
        listNeighbours.append('r0')
        listValues.append(graph['r0'])
    else:
        s1='n'
        s1 = s1+str(i)
        listNeighbours.append(s1)
        listValues.append(graph[s1])
'''
for i in range(0,no_of_neighbours):
    s1='n'
    s1 = s1+str(i)
    listNeighbours.append(s1)
    listValues.append(graph[s1])
#print(listNeighbours)
#print()
#print(listValues)
#print()

matrixValues = np.array(listValues)
#print(matrixValues)
#print()


def tsp(adjacency_matrix):
    G = nx.Graph()

    for i in range(len(adjacency_matrix)):
        for j in range(len(adjacency_matrix[i])):
            G.add_edge(i, j, weight=adjacency_matrix[i][j])

    optimal_path = list(nx.approximation.traveling_salesman_problem(G, cycle=False))

    cost = sum(adjacency_matrix[optimal_path[i]][optimal_path[i + 1]] for i in range(len(optimal_path) - 1))

    return optimal_path, cost

def save_output_to_json(output_path, vehicle_name, path):
    output_data = {vehicle_name: {"path": path}}
    with open(output_path, "w") as output_file:
        json.dump(output_data, output_file, indent=2)

optimal_path, cost = tsp(matrixValues)
#print(optimal_path)
print(json.dumps({"v0": {"path": ["r0"] + [f"n{i}" for i in optimal_path] + ["r0"]}}, indent=2))

output_file_path = 'level0_output.json'
save_output_to_json(output_file_path, "v0", ["r0"] + [f"n{i}" for i in optimal_path] + ["r0"])