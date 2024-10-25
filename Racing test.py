import networkx as nx
from collections import deque
import heapq

G = nx.Graph()

nodes = range(1, 11)
G.add_nodes_from(nodes)

edges = [
    (1, 2, 5), (1, 3, 2), (1, 4, 10), (1, 11, 7),   # New node 11 from start
    (2, 5, 1), (2, 12, 4),                         # Node 12 from node 2
    (3, 6, 8), (3, 13, 6),                         # Node 13 from node 3
    (4, 7, 2), (4, 14, 10),                        # Node 14 as a dead end
    (5, 8, 3), (5, 15, 15),                        # Node 15 as a long path
    (6, 9, 7), (6, 16, 12),                        # Node 16 as a complex path
    (7, 10, 1),                                    # Path to goal
    (8, 9, 1), (8, 17, 5),                         # Additional nodes from node 8
    (9, 10, 5),                                    # Path to goal
    (10, 18, 10),                                  # Dead end from goal node
    (11, 12, 5), (11, 16, 8),                      # Node 11 branching
    (12, 9, 10),                                   # Node 12 loops back to 9
    (13, 16, 9),                                   # Node 13 loops into the more complex path
    (14, 10, 15),                                  # A longer path to the goal
    (15, 16, 5),                                   # Node 15 connects to the complex path
    (16, 10, 20),                                  # Long route to the goal
    (17, 9, 4),                                    # Node 17 loops back into the path
    (18, 16, 25)                                   # Very long dead-end route
]

G.add_weighted_edges_from(edges)

player_paths = {
    "Malak": [1, 4, 7, 10],   
    "Bayoumi": [1, 2, 5, 8, 9, 10],  
    "Kahla": [1, 3, 6, 9, 10],   
    "Yasser": [1, 4, 7],  
}

player_scores = {
    "Malak": 19,
    "Bayoumi": 15,
    "Kahla": 22,
    "Yasser": float('inf'),  
}

def dfs_search(graph, start, goal):
    stack = [(start, [start], 0)] 

    while stack:
        node, path, cost = stack.pop()
        if node == goal:
            return path, cost  
        for neighbor in graph.neighbors(node):
            if neighbor not in path: 
                edge_weight = graph.edges[node, neighbor]["weight"]
                stack.append((neighbor, path + [neighbor], cost + edge_weight))

    return None, float('inf')  

def bfs_search(graph, start, goal):
    queue = deque([(start, [start], 0)]) 

    while queue:
        node, path, cost = queue.popleft()
        if node == goal:
            return path, cost  
        for neighbor in graph.neighbors(node):
            if neighbor not in path: 
                edge_weight = graph.edges[node, neighbor]["weight"]
                queue.append((neighbor, path + [neighbor], cost + edge_weight))

    return None, float('inf')  


def ucs_search(graph, start, goal):
    queue = [(0, start, [start])] 
    visited = set()

    while queue:
        cost, node, path = heapq.heappop(queue)
        if node == goal:
            return path, cost  

        if node not in visited:
            visited.add(node)
            for neighbor in graph.neighbors(node):
                if neighbor not in path:
                    edge_weight = graph.edges[node, neighbor]['weight']
                    heapq.heappush(queue, (cost + edge_weight, neighbor, path + [neighbor]))

    return None, float('inf') 

ai_path, ai_cost = dfs_search(G, 1, 10)

ai_score = ai_cost  

all_players_scores = {
    "Malak": player_scores["Malak"],
    "Bayoumi": player_scores["Bayoumi"],
    "Kahla": player_scores["Kahla"],
    "Yasser": player_scores["Yasser"],
    "AI Agent": ai_score
}

sorted_players = sorted(all_players_scores.items(), key=lambda x: x[1], reverse=False)

print("Racing Results :")
for player, score in sorted_players:
    if player == "AI Agent":
        print(f"{player}: Score {score}, Path {ai_path}")
    else:
        print(f"{player}: Score {score}, Path {player_paths[player]}")