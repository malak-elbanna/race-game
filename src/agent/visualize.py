import pydot
import networkx as nx
from IPython.display import Image, display

class Visualizer:
    def __init__(self):
        self.graph = nx.DiGraph()
    
    def add_state(self, parent, child, action):
        self.graph.add_edge(parent, child, action=action)

    def show_graph(self, solution=None):
        pydot_graph = nx.nx_pydot.to_pydot(self.graph)

        if solution:
            path_edges = []
            for i in range(len(solution) - 1):
                if solution[i] in self.graph and solution[i + 1] in self.graph:
                    path_edges.append((str(solution[i]), str(solution[i + 1])))  

            for edge in pydot_graph.get_edges():
                edge_src, edge_dst = edge.get_source(), edge.get_destination()
                if (edge_src, edge_dst) in path_edges:
                    edge.set_color("red")
                    edge.set_penwidth(2)

        pydot_graph.set_graph_defaults(rankdir="LR")  
        pydot_graph.set_node_defaults(shape="circle", style="filled", fillcolor="lightgrey") 

        pydot_graph.write_png("graph.png")
        display(Image(filename="graph.png"))

