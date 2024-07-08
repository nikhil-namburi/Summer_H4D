import networkx as nx
import numpy as np

class DynamicResourceGraph:
    def __init__(self, x, y, z, node_max, node_edge, distance_constant):
        self.graph = nx.DiGraph()
        self.node_max = node_max
        self.node_edge = node_edge
        self.distance_constant = distance_constant
        self.initialize_graph(x, y, z)

    def initialize_graph(self, x, y, z):
        # Create nodes
        self.graph.add_nodes_from(range(x))

        # Evenly distribute people and cars across nodes
        people_per_node = y // x
        cars_per_node = z // x

        for node in self.graph.nodes():
            self.graph.nodes[node]['people'] = people_per_node
            self.graph.nodes[node]['cars'] = cars_per_node
            self.graph.nodes[node]['max_capacity'] = self.node_max

        # Create edges with max capacity and distance
        for i in range(x):
            for j in range(x):
                if i != j:  # no self-loops
                    distance = np.random.randint(1, 10)  # Random distance between 1 and 10 units
                    travel_time = distance * self.distance_constant
                    self.graph.add_edge(i, j, max_capacity=self.node_edge, current_capacity=self.node_edge,
                                        distance=distance, travel_time=travel_time, flow=0)

    def update_resource_level(self, node, people_amount, cars_amount):
        """Update the people and cars level at a specific node."""
        self.graph.nodes[node]['people'] += people_amount
        self.graph.nodes[node]['cars'] += cars_amount

    def adjust_edge_capacities(self):
        """Adjust the capacities of edges dynamically based on current flow and resource availability."""
        for u, v in self.graph.edges():
            max_capacity = self.graph.edges[u, v]['max_capacity']
            current_flow = self.graph.edges[u, v]['flow']
            resource_availability = max_capacity - current_flow
            self.graph.edges[u, v]['current_capacity'] = resource_availability

    def move_resources(self, path, people_amount, cars_amount):
        """Move resources along a given path, updating flows and capacities."""
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]
            self.graph.edges[u, v]['flow'] += people_amount
            self.graph.edges[u, v]['current_capacity'] -= people_amount
            if self.graph.edges[u, v]['current_capacity'] < 0:
                raise ValueError("Capacity exceeded on edge ({}, {})".format(u, v))
            self.update_resource_level(u, -people_amount, -cars_amount)
            self.update_resource_level(v, people_amount, cars_amount)

    def reset_flows(self):
        """Reset the flow on all edges to zero (for simulation purposes)."""
        for u, v in self.graph.edges():
            self.graph.edges[u, v]['flow'] = 0
            self.graph.edges[u, v]['current_capacity'] = self.graph.edges[u, v]['max_capacity']

# Example usage
if __name__ == "__main__":
    x = 5  # Number of nodes
    y = 100  # Total number of people
    z = 20  # Total number of cars
    node_max = 50  # Max capacity of each node
    node_edge = 30  # Max capacity of each edge
    distance_constant = 1.5  # Constant to calculate traversal time

    graph = DynamicResourceGraph(x, y, z, node_max, node_edge, distance_constant)

    # Example of moving resources
    path = [0, 1, 2]
    people_to_move = 10
    cars_to_move = 2
    graph.move_resources(path, people_to_move, cars_to_move)

    # Adjust capacities based on current state
    graph.adjust_edge_capacities()

    # Print graph state for debugging
    print("Node attributes:")
    for node in graph.graph.nodes(data=True):
        print(node)

    print("Edge attributes:")
    for edge in graph.graph.edges(data=True):
        print(edge)
