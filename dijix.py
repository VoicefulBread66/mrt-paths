## code of implementation from https://www.udacity.com/blog/2021/10/implementing-dijkstras-algorithm-in-python.html

import sys
import math

# We create a class Graph. 
class Graph(object):
    # here init_graph is our data that goes into the Graph
    # so it just executes when the class 'Graph' is initiated, and then it would assign the properties nodes, call the construct_graph method and then save that result to the graph attribute of Graph
    def __init__(self, nodes, init_graph):
        self.nodes = nodes
        self.graph = self.construct_graph(nodes, init_graph)
    
    # The commentor states that "his method makes sure that the graph is symmetrical. In other words, if there's a path from node A to B with a value V, there needs to be a path from node B to node A with a value V."
    # so first, we declare a method called construct_graph...
    def construct_graph(self, nodes, init_graph):

        # creates a new dictionary called graph, then for every node as an input, it puts it into graph.
        graph = {}
        for node in nodes:
            graph[node] = {}
        
        # takes all our inputs and then updates it into the main graph
        graph.update(init_graph)
        
        # This just checks if a node is missing its reverse path, from A-B then from B-A, if it lacks it, the code adds one.

        for node, edges in graph.items():
            for adjacent_node, value in edges.items():
                #dictionary function, if it can get a path from adjacent node back to the original node, it would get it. If not, the default value it will return is the 2nd argument which is "False". Then it would be equal to false if the reverse path doesn't exist, so then the 2nd line will make that value exist :3
                if graph[adjacent_node].get(node, False) == False:
                    graph[adjacent_node][node] = value
        
        # returns the value of "graph"
        return graph
    
    def get_nodes(self):
        # Returns the nodes of the graph.
        return self.nodes
    
    def get_outgoing_edges(self, node):
        # Returns the neighbors of a node.
        connections = []
        for out_node in self.nodes:
            # loops through the nodes to find ones with connections and returns their values. dictionary function "get", if it can get a path from another node back to the original node, it would get it and NOT give "False" as an output, which is not equal to False. Therefore, it would be treated as a connection and added to connections
            # If not, the default value it will return is the 2nd argument which is "False". Then it would be equal to false and not be added 

            if self.graph[node].get(out_node, False) != False:
                connections.append(out_node)
        return connections
    
    def value(self, node1, node2):
        # Returns the value of an edge between two nodes.
        return self.graph[node1][node2]
    

def dijkstra_algorithm(graph, start_node):
    # puts everything in unvisited nodes. 
    unvisited_nodes = list(graph.get_nodes())
 
    # We'll use this dict to save the cost of visiting each node and update it as we move along the graph   
    shortest_path = {}
 
    # We'll use this dict to save the shortest known path to a node found so far
    previous_nodes = {}
 
    # We'll use max_value to initialize the "infinity" value of the unvisited nodes
    # To make things simple, maxsize is 9223372036854775807 which is a very large number. For all itents and purposes this SHOULD be enough to count as infinity unless we are travelling to the next star or something.    
    max_value = math.inf

    # just goes for every node in unvisited_nodes, it puts in the shortest_path array the infinity value for the shortest distance from the start node. 
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    
    # However, we initialize the starting node's value with 0, because obviously no work needs to be done to move from the start to the start. 
    shortest_path[start_node] = 0
    
    # The algorithm executes until we visit all nodes. Which means while there is something in unvisited_nodes array, this code will run.
    while unvisited_nodes:
        # The code block below finds the node with the lowest score
        current_min_node = None

        # iterates over all unvisited nodes
        for node in unvisited_nodes: 
            # so if there's nothing saved in Current_Min_Node, it will automatically save the first value. Then if it finds another node with a shorter path from the start node, it saves that to current_min_node.
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node

                
        # Gets the current node's neighbours
        neighbors = graph.get_outgoing_edges(current_min_node)

        # loops through each of the current node's neighbours
        for neighbor in neighbors:
            # makes a tentative value consisting of = shortest path from start to current node + neighbour of current node
            tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)

            # if our new value is smaller than the existing value which would usually be stupidly large because of the sysmax thing, we replace it and update the best path.
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbor] = current_min_node
 
        # After visiting its neighbors, we mark the node as "visited"
        # Loops over and over until we've got everything
        unvisited_nodes.remove(current_min_node)
    
    return previous_nodes, shortest_path

#just prints the results
def print_result(previous_nodes, shortest_path, start_node, target_node):
    path = []
    node = target_node
    
    while node != start_node:
        path.append(node)
        node = previous_nodes[node]
 
    # Add the start node manually
    path.append(start_node)
    
    spath_min = math.floor(shortest_path[target_node] / 60)
    spath_sec = shortest_path[target_node] % 60

    route = f"Shortest path shown, with cost of {spath_min} minutes and {spath_sec} seconds. " + str(" -> ".join(reversed(path)))

    path = list(reversed(path))
    # print(path)

    interchanges = []
    for i in range(len(path) - 1):
        checkone = str(path[i])[:3]
        checktwo = str(path[i+1])[:3]
        if (checkone != checktwo):
            interchanges.append(f"Change lines from {checkone} to {checktwo} at {path[i][4:]}")

    return [path, shortest_path[target_node], interchanges]