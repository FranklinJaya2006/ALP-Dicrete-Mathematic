import matplotlib.pyplot as plt
import networkx as nx

class Siklus:
    def __init__(self):
        self.circuit = nx.Graph()

    def circuit_to_formula(self):
        formula = nx.Graph()
        for node, data in self.circuit.nodes(data=True):
            formula.add_node(node, label=data["label"])
        for u, v in self.circuit.edges():
            formula.add_edge(u, v)
        return formula

    def formula_to_string(self, formula):
        def _to_string(formula, node, visited):
            if node in visited:
                return ""
            visited.add(node)
            label = formula.nodes[node]["label"]
            neighbors = list(formula[node])
            if not neighbors:
                return label
            subformulas = [_to_string(formula, n, visited) for n in neighbors]
            subformulas = [sf for sf in subformulas if sf]
            if len(subformulas) == 1:
                return f"{label}({subformulas[0]})"
            return f"({f' {label} '.join(subformulas)})"

        visited = set()
        root = next(iter(formula.nodes))
        return _to_string(formula, root, visited)

    def add_nodes(self):
        self.circuit.add_node(1, label="∧")
        self.circuit.add_node(2, label="∨")
        self.circuit.add_node(3, label="¬")
        self.circuit.add_node(4, label="A")
        self.circuit.add_node(5, label="B")
        self.circuit.add_node(6, label="C")

    def add_edges(self):
        self.circuit.add_edge(1, 2)
        self.circuit.add_edge(1, 3)
        self.circuit.add_edge(2, 4)
        self.circuit.add_edge(2, 5)
        self.circuit.add_edge(3, 6)
        self.circuit.add_edge(5, 1)

    def gabungs(self):
        self.add_nodes()
        self.add_edges()

    def find_cycle(self):
        def dfs(v, parent, visited, stack):
            visited.add(v)
            stack.append(v)
            for neighbor in self.circuit[v]:
                if neighbor == parent:
                    continue
                if neighbor in visited:
                    return stack[stack.index(neighbor):]
                cycle = dfs(neighbor, v, visited, stack)
                if cycle:
                    return cycle
            stack.pop()
            return None

        visited = set()
        for node in self.circuit.nodes:
            if node not in visited:
                cycle = dfs(node, None, visited, [])
                if cycle:
                    return cycle
        return None

    def visualize_circuit(self):
        self.gabungs()
        cycle = self.find_cycle()
        if cycle:
            print(f"Siklus ditemukan: {cycle}")
        else:
            print("Tidak ada siklus dalam graf")

        formula = self.circuit_to_formula()
        formula_string = self.formula_to_string(formula)
        print(f"Formula: {formula_string}")

        labels = nx.get_node_attributes(self.circuit, "label")
        options = {"node_size": 600, "alpha": 0.5, "node_color": "blue", "font_size": 22}
        plt.figure(figsize=(8, 8))
        pos = nx.spring_layout(self.circuit)
        nx.draw_networkx(self.circuit, pos, **options)
        nx.draw_networkx_labels(self.circuit, pos, labels=labels)
        plt.title(formula_string)
        plt.axis("equal")
        plt.show()
