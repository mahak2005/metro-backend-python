import csv
from collections import deque
from math import radians, sin, cos, sqrt, atan2

from util.CsvParser import CsvParser
from util.DijkstraAlgorithm import DijkstraAlgorithm
from util.DijkstraAlgorithm2 import DijkstraAlgorithm2
from model.MetroGraph import MetroGraph
from model.MetroRoute import MetroRoute
from model.MetroShape import MetroShape
from model.MetroStop import MetroStop
from model.MetroStopTime import MetroStopTime
from model.MetroTrip import MetroTrip
from EdgeWeightCalculator import EdgeWeightCalculator
import csv
from collections import defaultdict, deque
import math

class MetroNetworkAnalysis:

    @staticmethod
    def main():
        try:
            # Open the files using 'with' to ensure they are closed after reading
            with open("data/route.csv", "r", newline='', encoding='utf-8') as routes_stream:
                routes_reader = csv.reader(routes_stream)
                routes = CsvParser.parse_routes(routes_reader)

            with open("data/stop.csv", "r", newline='', encoding='utf-8') as stops_stream:
                stops_reader = csv.reader(stops_stream)
                stops = CsvParser.parse_stops(stops_reader)

            with open("data/trip.csv", "r", newline='', encoding='utf-8') as trips_stream:
                trips_reader = csv.reader(trips_stream)
                trips = CsvParser.parse_trips(trips_reader)

            with open("data/stop_time.csv", "r", newline='', encoding='utf-8') as stop_times_stream:
                stop_times_reader = csv.reader(stop_times_stream)
                stop_times = CsvParser.parse_stop_times(stop_times_reader)

            with open("data/shape.csv", "r", newline='', encoding='utf-8') as shapes_stream:
                shapes_reader = csv.reader(shapes_stream)
                shapes = CsvParser.parse_shapes(shapes_reader)


            # Create the graph
            graph = MetroGraph()

            # Populate graph with data from parsed CSV files
            stop_id_to_name = {}  # Map to store stop ID to stop name
            for stop in stops.values():
                graph.addStop(stop.getStopId(), stop.getStopName(), stop.getLatitude(), stop.getLongitude())
                stop_id_to_name[stop.getStopId()] = stop.getStopName()

            # Group shapes by shapeId and sort by sequence
            shape_groups = MetroNetworkAnalysis.groupShapesById(shapes)

            # Sort the shape points based on their sequence for each shapeId
            for shape_list in shape_groups.values():
                shape_list.sort(key=lambda shape: shape.getSequence())

            # User input
            choice = int(input("Select the edge weight for Dijkstra's algorithm: 1 for Distance, 2 for Time, 3 for BFS, 4 for DFS"))
            start_stop_id = input("Enter the start stop ID: ")
            end_stop_id = input("Enter the end stop ID: ")

            print("Available stops in the graph:")
            for stop_id in graph.get_all_stops():
                print(stop_id)


            # Check if stops exist
            # if start_stop_id not in graph or end_stop_id not in graph:
            #     print("Invalid stop IDs entered.")
            #     return

            distances = {}
            path = []

            if choice == 1:  # Distance-based Dijkstra
                for shape_sequence in shape_groups.values():
                    previous_stop = None
                    for shape in shape_sequence:
                        current_stop = MetroNetworkAnalysis.findClosestStop(stops, shape.getLatitude(), shape.getLongitude(), 3.0)
                        if current_stop:
                            if previous_stop and previous_stop.getStopId() != current_stop.getStopId():
                                distance = MetroNetworkAnalysis.calculateDistance(previous_stop.getLatitude(), previous_stop.getLongitude(), current_stop.getLatitude(), current_stop.getLongitude())
                                graph.addEdge(previous_stop.getStopId(), current_stop.getStopId(), distance)
                            previous_stop = current_stop
                MetroNetworkAnalysis.addManualEdge(stops, graph)

                dijkstra = DijkstraAlgorithm()
                distances = dijkstra.dijkstra(graph, start_stop_id)
                path = dijkstra.getPath(end_stop_id, DijkstraAlgorithm.previousStops)

                if distances.get(end_stop_id) != float("inf"):
                    path_with_names = [stop_id_to_name.get(stop_id, stop_id) for stop_id in path]
                    print(f"The shortest distance from {stop_id_to_name.get(start_stop_id)} to {stop_id_to_name.get(end_stop_id)} is {distances.get(end_stop_id)}")
                    print(f"The path is: {' -> '.join(path_with_names)}")
                else:
                    print(f"No path found between {start_stop_id} and {end_stop_id}")

            elif choice == 2:  # Time-based Dijkstra
                for shape_sequence in shape_groups.values():
                    previous_stop = None
                    for shape in shape_sequence:
                        current_stop = MetroNetworkAnalysis.findClosestStop(stops, shape.getLatitude(), shape.getLongitude(), 3.0)
                        if current_stop:
                            if previous_stop and previous_stop.getStopId() != current_stop.getStopId():
                                edge_weight = EdgeWeightCalculator.getEdgeWeight(stop_times, previous_stop.getStopId(), current_stop.getStopId())
                                graph.addEdge(previous_stop.getStopId(), current_stop.getStopId(), edge_weight)
                            previous_stop = current_stop
                MetroNetworkAnalysis.addManualEdge(stops, graph)

                dijkstra = DijkstraAlgorithm2()
                distances = dijkstra.dijkstra(graph, start_stop_id, stop_times)
                path = dijkstra.getPath(end_stop_id)

                if distances.get(end_stop_id) != float("inf"):
                    path_with_names = [stop_id_to_name.get(stop_id, stop_id) for stop_id in path]
                    print(f"The shortest time from {stop_id_to_name.get(start_stop_id)} to {stop_id_to_name.get(end_stop_id)} is {distances.get(end_stop_id)}")
                    print(f"The path is: {' -> '.join(path_with_names)}")
                else:
                    print(f"No path found between {start_stop_id} and {end_stop_id}")

            elif choice == 3 or choice == 4:
                for shape_sequence in shape_groups.values():
                    previous_stop = None
                    for shape in shape_sequence:
                        current_stop = MetroNetworkAnalysis.findClosestStop(stops, shape.getLatitude(), shape.getLongitude(), 3.0)
                        if current_stop:
                            if previous_stop and previous_stop.getStopId() != current_stop.getStopId():
                                distance = MetroNetworkAnalysis.calculateDistance(previous_stop.getLatitude(), previous_stop.getLongitude(), current_stop.getLatitude(), current_stop.getLongitude())
                                graph.addEdge(previous_stop.getStopId(), current_stop.getStopId(), distance)
                            previous_stop = current_stop

                if choice == 3:
                    bfs_path = MetroNetworkAnalysis.bfs(graph, start_stop_id, end_stop_id, stop_id_to_name)
                    if bfs_path:
                        print(f"The path found using BFS is: {' -> '.join(bfs_path)}")
                    else:
                        print("No path found using BFS.")
                if choice == 4:
                    dfs_path = MetroNetworkAnalysis.dfs(graph, start_stop_id, end_stop_id, stop_id_to_name, set())
                    if dfs_path:
                        print(f"The path found using DFS is: {' -> '.join(dfs_path)}")
                    else:
                        print("No path found using DFS.")

            else:
                print("Invalid choice. Please select 1, 2, 3 or 4")
                return

        except Exception as e:
            print(e)

    @staticmethod
    def bfs(graph, start, end, stop_id_to_name):
        queue = deque([start])
        previous = {start: None}

        while queue:
            current = queue.popleft()
            if current == end:
                return MetroNetworkAnalysis.constructPath(previous, start, end, stop_id_to_name)

            for neighbor in graph.getNeighbors(current).keys():
                if neighbor not in previous:
                    queue.append(neighbor)
                    previous[neighbor] = current
        return []

    @staticmethod
    def dfs(graph, start, end, stop_id_to_name, visited):
        stack = [start]
        previous = {start: None}
        visited.add(start)

        while stack:
            current = stack.pop()
            if current == end:
                return MetroNetworkAnalysis.constructPath(previous, start, end, stop_id_to_name)

            for neighbor in graph.getNeighbors(current).keys():
                if neighbor not in visited:
                    stack.append(neighbor)
                    visited.add(neighbor)
                    previous[neighbor] = current
        return []

    @staticmethod
    def constructPath(previous, start, end, stop_id_to_name):
        path = []
        for at in [end]:
            while at is not None:
                path.append(stop_id_to_name.get(at, at))
                at = previous.get(at)
        return path[::-1]

    @staticmethod
    def findClosestStop(stops, latitude, longitude, tolerance_km):
        closest_stop = None
        min_distance = float("inf")

        for stop in stops.values():
            distance = MetroNetworkAnalysis.calculateDistance(latitude, longitude, stop.getLatitude(), stop.getLongitude())
            if distance <= tolerance_km and distance < min_distance:
                min_distance = distance
                closest_stop = stop

        if closest_stop is None:
            print(f"No stop found for lat: {latitude}, lon: {longitude} within tolerance: {tolerance_km} km")

        return closest_stop

    @staticmethod
    def calculateDistance(lat1, lon1, lat2, lon2):
        R = 6371  # Radius of Earth in km
        lat_distance = math.radians(lat2 - lat1)
        lon_distance = math.radians(lon2 - lon1)

        a = math.sin(lat_distance / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(lon_distance / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c  # Return in km

    @staticmethod
    def groupShapesById(shapes):
        shape_groups = defaultdict(list)
        for shape in shapes.values():
            shape_groups[shape.getShapeId()].append(shape)
        return shape_groups

    @staticmethod
    def addManualEdge(stops, graph):
        stop205 = stops.get("205")
        closest_neighbor = MetroNetworkAnalysis.findClosestStop(stops, 28.570606, 77.182838, 0.5)  # Example closest neighbor
        if stop205 and closest_neighbor:
            graph.addEdge(stop205.getStopId(), closest_neighbor.getStopId(), MetroNetworkAnalysis.calculateDistance(stop205.getLatitude(), stop205.getLongitude(), closest_neighbor.getLatitude(), closest_neighbor.getLongitude()))

if __name__ == "__main__":
    MetroNetworkAnalysis.main()
