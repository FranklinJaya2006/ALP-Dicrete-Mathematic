from graf_circuit_tak_berarah import Siklus
from graf_circuit_berarah import run_all
from graf_shortest_berarah import Graf
from graf_shortest_tak_berarah import Gruf
from Krackhardt_Centrality import Krack
from maximumindependentgraph import Max
import networkx as nx
from subgraph import GraphPartitioner
import matplotlib.pyplot as plt

def main():
    # Membuat objek Siklus
    print("\n Circuit tak berarah")
    siklus = Siklus()
    
    # Menjalankan metode visualisasi siklus
    siklus.visualize_circuit()
    
    print("\n Circuit berarah")
    run_all()
    
    print("\n Shortest berarah")
    graph = Graf()
    graph.gabungs()
    graph.visualize_graph()
    
    print("\n Shortest tak berarah")
    gruph = Gruf()
    gruph.gabungs()
    gruph.visualize_graph()
    
    print("\n Krackhardt Centrality")
    krack = Krack()
    krack.runkrack()
    
    print("\n Maximum Independent Graph")
    max = Max()
    max.maximum()
    
    print("\n Subgraph")
    G_ex = nx.DiGraph()
    G_ex.add_nodes_from(["In"], node_type="input", node_color="b")
    G_ex.add_nodes_from(["A", "C", "E", "F"], node_type="supported", node_color="g")
    G_ex.add_nodes_from(["B", "D"], node_type="unsupported", node_color="r")
    G_ex.add_nodes_from(["Out"], node_type="output", node_color="m")
    G_ex.add_edges_from(
        [
            ("In", "A"),
            ("A", "B"),
            ("B", "C"),
            ("B", "D"),
            ("D", "E"),
            ("C", "F"),
            ("E", "F"),
            ("F", "Out"),
        ]
    )

    # Membuat instance GraphPartitioner dan memanggil fungsi
    partitioner = GraphPartitioner(G_ex)
    partitioner.plot_graph()  # Plot graf awal

    subgraphs_of_G_ex, removed_edges = partitioner.graph_partitioning(plotting=True)

    # Plot subgraf yang terpisah
    for subgraph in subgraphs_of_G_ex:
        _pos = nx.spring_layout(subgraph)
        plt.figure(figsize=(8, 8))
        nx.draw_networkx_edges(subgraph, _pos, alpha=0.3, edge_color="k")
        node_color_list_c = [nc for _, nc in subgraph.nodes(data="node_color")]
        nx.draw_networkx_nodes(subgraph, _pos, node_color=node_color_list_c)
        nx.draw_networkx_labels(subgraph, _pos, font_size=14)
        plt.axis("off")
        plt.title("One of the subgraphs.")
        plt.show()

    # Rekonstruksi graf dan plot
    partitioner.reconstruct_graph(subgraphs_of_G_ex, removed_edges)

if __name__ == "__main__":
    main()
