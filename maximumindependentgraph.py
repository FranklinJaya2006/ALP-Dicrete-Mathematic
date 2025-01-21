import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import approximation as approx

class Max:
    @staticmethod
    def maximum():
        # Define the graph
        G = nx.Graph(
            [
                (1, 2),
                (7, 2),
                (3, 9),
                (3, 2),
                (7, 6),
                (5, 2),
                (1, 5),
                (2, 8),
                (10, 2),
                (1, 7),
                (6, 1),
                (6, 9),
                (8, 4),
                (9, 4),
            ]
        )

        # Compute the maximum independent set
        I = approx.maximum_independent_set(G)
        print(f"Maximum independent set of G: {I}")

        pos = nx.spring_layout(G, iterations=100, seed=42)

        edge_colors = [
            "red" if u in I or v in I else "gray" for u, v in G.edges
        ]

        # Draw the graph with highlighted edges
        plt.figure(figsize=(8, 6))
        nx.draw(
            G,
            pos=pos,
            with_labels=True,
            node_color=["tab:red" if n in I else "tab:blue" for n in G],
            node_size=800,
            font_size=10,
            font_color="white",
            edge_color=edge_colors,
            width=2,
        )

        # Show the graph
        plt.title("Graph with Highlighted Maximum Independent Set and Edges")
        plt.show()
