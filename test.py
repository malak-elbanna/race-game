import networkx as nx

# Define the graph
G = nx.Graph()

# Define the edges with their weights
edges = [
    (1, 2, 50),  # Made path more expensive
    (1, 3, 20),  # Made path more expensive
    (1, 4, 100), # Very expensive now
    (1, 11, 70), # Longer route made very expensive
    (2, 5, 10),  # Increased the cost slightly
    (2, 12, 40), # More expensive
    (3, 6, 30),  # Increased to make it costly
    (3, 13, 60), # Longer and more expensive
    (4, 7, 20),  # Kept it moderate but not optimal
    (4, 14, 150),# Dead end very costly
    (5, 8, 15),  # Increased cost
    (5, 15, 100),# Long route made very expensive
    (6, 9, 40),  # Expensive now
    (6, 16, 80), # Another long and costly route
    (7, 10, 10), # Increased, not optimal
    (8, 9, 20),  # Increased cost to push away from optimal path
    (8, 17, 50), # Not optimal anymore
    (9, 10, 5),  # This becomes the shortest path now
    (10, 18, 100), # Dead end very expensive
    (11, 12, 60), # Expensive
    (11, 16, 80), # Long, expensive
    (12, 9, 90),  # Expensive path
    (13, 16, 100),# Expensive, longer
    (14, 10, 200),# Very long and expensive
    (15, 16, 90), # Long path
    (16, 10, 300),# Very costly long path
    (17, 9, 10),  # Dead end moderately cheap
    (18, 16, 250) # Dead end very costly
]

# Add edges to the graph
G.add_weighted_edges_from(edges)

# Use Dijkstra's algorithm to find the shortest path from node 1 to 10
shortest_path = nx.dijkstra_path(G, source=1, target=10)
shortest_path_length = nx.dijkstra_path_length(G, source=1, target=10)

# Find second and third shortest paths
all_paths = list(nx.all_simple_paths(G, source=1, target=10))
all_paths_with_costs = []

# Calculate the cost for each path
for path in all_paths:
    cost = sum(G.edges[path[i], path[i+1]]['weight'] for i in range(len(path)-1))
    all_paths_with_costs.append((path, cost))

# Sort the paths by cost
sorted_paths = sorted(all_paths_with_costs, key=lambda x: x[1])

# Print the 3 shortest paths and their costs
for i, (path, cost) in enumerate(sorted_paths[:4]):
    print(f"Path {i+1}: {path}, Cost: {cost}")
