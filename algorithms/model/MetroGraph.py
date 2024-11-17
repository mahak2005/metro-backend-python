class MetroStop:
    def __init__(self, stop_id, name, latitude, longitude):
        self.stop_id = stop_id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f"MetroStop(id={self.stop_id}, name={self.name}, latitude={self.latitude}, longitude={self.longitude})"


class MetroGraph:
    def __init__(self):
        self.stops = {}  # Map to store stops by their ID
        self.adjacency_list = {}  # Adjacency list to store connections between stops

    def addStop(self, stop_id, name, latitude, longitude):
        """Add a stop to the graph."""
        self.stops[stop_id] = MetroStop(stop_id, name, latitude, longitude)
        self.adjacency_list[stop_id] = {}  # Initialize adjacency list for the stop

    def addEdge(self, from_stop_id, to_stop_id, weight):
        """Add an edge (connection) between two stops with a weight (e.g., travel time)."""
        if from_stop_id in self.adjacency_list and to_stop_id in self.adjacency_list:
            self.adjacency_list[from_stop_id][to_stop_id] = weight
            self.adjacency_list[to_stop_id][from_stop_id] = weight  # For undirected graph

    def set_distance(self, from_stop_id, to_stop_id, distance):
        """Set or update the distance between two stops."""
        if from_stop_id in self.adjacency_list and to_stop_id in self.adjacency_list:
            self.adjacency_list[from_stop_id][to_stop_id] = distance
            self.adjacency_list[to_stop_id][from_stop_id] = distance  # For undirected graph
        else:
            print("One or both stops do not exist in the graph.")

    def containsStop(self, stop_id):
        """Check if a stop exists in the graph."""
        return stop_id in self.stops

    def get_all_stops(self):
        """Get all stop IDs."""
        return self.stops.keys()

    def get_neighbors(self, stop_id):
        """Get all neighbors (connections) for a given stop."""
        return self.adjacency_list.get(stop_id, {})

    def get_stop(self, stop_id):
        """Get the details of a specific stop."""
        return self.stops.get(stop_id)

    # Define the __iter__ method to iterate over the stops
    def __iter__(self):
        """Make MetroGraph iterable over its stops."""
        return iter(self.stops.values())  # Iterating over the MetroStop objects

# Example usage
# metro_graph = MetroGraph()
# metro_graph.add_stop("S1", "Station 1", 28.7041, 77.1025)
# metro_graph.add_stop("S2", "Station 2", 28.7050, 77.1035)
# metro_graph.add_edge("S1", "S2", 5.0)  # Example: travel time between two stops
# metro_graph.set_distance("S1", "S2", 5.0)

# print(metro_graph.get_stop("S1"))
# print(metro_graph.get_neighbors("S1"))
