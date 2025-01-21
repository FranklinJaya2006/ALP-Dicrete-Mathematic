import networkx as nx
import matplotlib.pyplot as plt

class Gruf:
    def __init__(self):
        self.graph = nx.Graph()  
    
    def add_nodes(self):
        self.graph.add_node(1)
        self.graph.add_node(2)
        self.graph.add_node(3)
        self.graph.add_node(4)
        self.graph.add_node(5)
        print("Node berhasil ditambahkan!")
        
    def add_edges(self):
        self.graph.add_edge(1, 2, weight=4.5)
        self.graph.add_edge(1, 3, weight=3.2)
        self.graph.add_edge(2, 4, weight=2.7)
        self.graph.add_edge(3, 4, weight=1.8)
        self.graph.add_edge(1, 4, weight=6.7)
        self.graph.add_edge(3, 5, weight=2.7)
        print("Edge berhasil ditambahkan!")
        
    def gabungs(self):
        self.add_nodes()
        self.add_edges()

    def visualize_graph(self):
        pende = nx.shortest_path(self.graph, source=1, target=5, weight='weight')
        print(f"Jalur terpendek dari 1 ke 5: {pende}")
        pendeks = list(zip(pende, pende[1:]))
        
        edge_colors = [
            "red" if edge in pendeks or tuple(reversed(edge)) in pendeks else "black"
            for edge in self.graph.edges()
        ]
        
        pos = nx.spring_layout(self.graph)
        
        nx.draw_networkx_nodes(self.graph, pos)
        nx.draw_networkx_edges(self.graph, pos, edge_color=edge_colors)
        nx.draw_networkx_labels(self.graph, pos)
        nx.draw_networkx_edge_labels(
            self.graph, pos, edge_labels={(u, v): d["weight"] for u, v, d in self.graph.edges(data=True)}
        )

        plt.show()


