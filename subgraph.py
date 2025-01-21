import networkx as nx
import matplotlib.pyplot as plt

class GraphPartitioner:
    def __init__(self, G):
        """Menerima graf yang akan dipartisi."""
        self.G = G

    def graph_partitioning(self, plotting=True):
        """Mempartisi graf menjadi subgraf berdasarkan tipe node."""
        # Kategorikan node berdasarkan atribut node_type mereka
        supported_nodes = {n for n, d in self.G.nodes(data="node_type") if d == "supported"}
        unsupported_nodes = {n for n, d in self.G.nodes(data="node_type") if d == "unsupported"}

        # Salin graf
        H = self.G.copy()
        # Hapus semua edge yang menghubungkan node yang didukung dan yang tidak didukung
        H.remove_edges_from(
            (n, nbr, d)
            for n, nbrs in self.G.adj.items()
            if n in supported_nodes
            for nbr, d in nbrs.items()
            if nbr in unsupported_nodes
        )
        H.remove_edges_from(
            (n, nbr, d)
            for n, nbrs in self.G.adj.items()
            if n in unsupported_nodes
            for nbr, d in nbrs.items()
            if nbr in supported_nodes
        )

        # Kumpulkan semua edge yang dihapus untuk rekonstruksi
        G_minus_H = nx.DiGraph()
        G_minus_H.add_edges_from(set(self.G.edges) - set(H.edges))

        if plotting:
            # Plot graf yang telah dipangkas dengan edge yang dihapus
            _node_colors = [c for _, c in H.nodes(data="node_color")]
            _pos = nx.spring_layout(H)
            plt.figure(figsize=(8, 8))
            nx.draw_networkx_edges(H, _pos, alpha=0.3, edge_color="k")
            nx.draw_networkx_nodes(H, _pos, node_color=_node_colors)
            nx.draw_networkx_labels(H, _pos, font_size=14)
            plt.axis("off")
            plt.title("The stripped graph with the edges removed.")
            plt.show()
            # Plot edge yang dihapus
            _pos = nx.spring_layout(G_minus_H)
            plt.figure(figsize=(8, 8))
            ncl = [self.G.nodes[n]["node_color"] for n in G_minus_H.nodes]
            nx.draw_networkx_edges(G_minus_H, _pos, alpha=0.3, edge_color="k")
            nx.draw_networkx_nodes(G_minus_H, _pos, node_color=ncl)
            nx.draw_networkx_labels(G_minus_H, _pos, font_size=14)
            plt.axis("off")
            plt.title("The removed edges.")
            plt.show()

        # Temukan komponen yang terhubung dalam graf tak terarah yang dipangkas
        subgraphs = [
            H.subgraph(c).copy() for c in nx.connected_components(H.to_undirected())
        ]

        return subgraphs, G_minus_H

    def plot_graph(self):
        """Plot graf awal sebelum dipartisi."""
        node_color_list = [nc for _, nc in self.G.nodes(data="node_color")]
        pos = nx.spectral_layout(self.G)
        plt.figure(figsize=(8, 8))
        nx.draw_networkx_edges(self.G, pos, alpha=0.3, edge_color="k")
        nx.draw_networkx_nodes(self.G, pos, alpha=0.8, node_color=node_color_list)
        nx.draw_networkx_labels(self.G, pos, font_size=14)
        plt.axis("off")
        plt.title("The original graph.")
        plt.show()

    def reconstruct_graph(self, subgraphs, removed_edges):
        """Rekonstruksi graf dari subgraf dan edge yang dihapus."""
        G_reconstructed = nx.DiGraph()
        for subgraph in subgraphs:
            G_reconstructed = nx.compose(G_reconstructed, subgraph)
        G_reconstructed.add_edges_from(removed_edges.edges())

        assert nx.is_isomorphic(self.G, G_reconstructed)

        node_color_list = [nc for _, nc in G_reconstructed.nodes(data="node_color")]
        pos = nx.spectral_layout(G_reconstructed)
        plt.figure(figsize=(8, 8))
        nx.draw_networkx_edges(G_reconstructed, pos, alpha=0.3, edge_color="k")
        nx.draw_networkx_nodes(G_reconstructed, pos, alpha=0.8, node_color=node_color_list)
        nx.draw_networkx_labels(G_reconstructed, pos, font_size=14)
        plt.axis("off")
        plt.title("The reconstructed graph.")
        plt.show()
