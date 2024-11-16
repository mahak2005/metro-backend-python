import collections
import math
from typing import List, Dict, Set
import csv
from collections import deque
from math import radians, sin, cos, sqrt, atan2
from flask import Flask
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

class MetroNetworkService:

    def __init__(self, choice: int) -> None:
        self.graph = None
        self.stopIdToName = {}
        self.stopTimes = {}
        self.initializeGraph(choice)

    def initializeGraph(self, choice: int) -> None:
        # Simulating the InputStream and file parsing process
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
        self.graph = MetroGraph()
        self.stopIdToName = {}

        # Populate graph with data from parsed CSV files
        for stop in stops.values():
            self.graph.addStop(stop.getStopId(), stop.getStopName(), stop.getLatitude(), stop.getLongitude())
            self.stopIdToName[stop.getStopId()] = stop.getStopName()

        # Group shapes by shapeId and sort by sequence
        shapeGroups = self.groupShapesById(shapes)
        for shapeList in shapeGroups.values():
            shapeList.sort(key=lambda shape: shape.getSequence())

        # Add edges to the graph based on the passed choice
        self.addEdgesToGraph(shapeGroups, stops, self.stopTimes, choice)

    def addEdgesToGraph(self, shapeGroups: Dict[str, List['MetroShape']], stops: Dict[str, 'MetroStop'],
                        stopTimes: Dict[str, 'MetroStopTime'], choice: int) -> None:
        for shapeSequence in shapeGroups.values():
            previousStop = None

            for currentShape in shapeSequence:
                # Find the closest stop to the current shape point
                currentStop = self.findClosestStop(stops, currentShape.getLatitude(), currentShape.getLongitude(), 3.0)

                if currentStop is not None:
                    if previousStop is not None and previousStop.getStopId() != currentStop.getStopId():
                        if choice == 1:
                            edgeWeight = self.calculateDistance(previousStop.getLatitude(), previousStop.getLongitude(), currentStop.getLatitude(), currentStop.getLongitude())
                            self.graph.addEdge(previousStop.getStopId(), currentStop.getStopId(), edgeWeight)
                        elif choice == 2:
                            edgeWeight = EdgeWeightCalculator.getEdgeWeight(stopTimes, previousStop.getStopId(), currentStop.getStopId())
                            self.graph.addEdge(previousStop.getStopId(), currentStop.getStopId(), edgeWeight)
                        else:
                            edgeWeight = self.calculateDistance(previousStop.getLatitude(), previousStop.getLongitude(), currentStop.getLatitude(), currentStop.getLongitude())
                            self.graph.addEdge(previousStop.getStopId(), currentStop.getStopId(), edgeWeight)
                    previousStop = currentStop

        stop205 = stops.get("205")
        closestNeighbor = self.findClosestStop(stops, 28.570606, 77.182838, 3.0)

        if stop205 is not None and closestNeighbor is not None:
            self.graph.addEdge(stop205.getStopId(), closestNeighbor.getStopId(),
                               self.calculateDistance(stop205.getLatitude(), stop205.getLongitude(),
                                                      closestNeighbor.getLatitude(), closestNeighbor.getLongitude()))

    def findShortestPath(self, startStopId: str, endStopId: str, choice: int) -> str:
        if not self.graph.containsStop(startStopId) or not self.graph.containsStop(endStopId):
            return "Invalid stop IDs entered."
        
        distances = None
        path = None

        if choice == 1:
            dijkstra = DijkstraAlgorithm()
            distances = dijkstra.dijkstra(self.graph, startStopId)
            path = dijkstra.getPath(endStopId, DijkstraAlgorithm.previousStops)
        elif choice == 2:
            dijkstra = DijkstraAlgorithm2()
            distances = dijkstra.dijkstra(self.graph, startStopId, self.stopTimes)
            path = dijkstra.getPath(endStopId)
        elif choice == 3:
            bfsPath = self.bfs(self.graph, startStopId, endStopId)
            return f"The path found using BFS is: {' -> '.join(bfsPath)}"
        elif choice == 4:
            dfsPath = self.dfs(self.graph, startStopId, endStopId, set())
            return f"The path found using DFS is: {' -> '.join(dfsPath)}"
        else:
            return "Invalid choice. Please select 1, 2, 3 or 4"

        if distances[endStopId] != float('inf'):
            pathWithNames = [self.stopIdToName.get(stopId, stopId) for stopId in path]
            if choice == 1:
                return f"The shortest path from {self.stopIdToName.get(startStopId)} to {self.stopIdToName.get(endStopId)} is:\n{' -> '.join(pathWithNames)}.\nThe shortest distance from {self.stopIdToName.get(startStopId)} to {self.stopIdToName.get(endStopId)} is {distances[endStopId]}"
            else:
                return f"The shortest path from {self.stopIdToName.get(startStopId)} to {self.stopIdToName.get(endStopId)} is:\n{' -> '.join(pathWithNames)}.\nThe shortest time from {self.stopIdToName.get(startStopId)} to {self.stopIdToName.get(endStopId)} is {distances[endStopId]}"
        else:
            return f"No path found between {startStopId} and {endStopId}"

    def bfs(self, graph: 'MetroGraph', start: str, end: str) -> List[str]:
        queue = collections.deque([start])
        previous = {start: None}

        while queue:
            current = queue.popleft()
            if current == end:
                return self.constructPath(previous, start, end)

            for neighbor in graph.get_neighbors(current).keys():
                if neighbor not in previous:
                    queue.append(neighbor)
                    previous[neighbor] = current
        return []

    def dfs(self, graph: 'MetroGraph', start: str, end: str, visited: Set[str]) -> List[str]:
        stack = [start]
        previous = {start: None}
        visited.add(start)

        while stack:
            current = stack.pop()
            if current == end:
                return self.constructPath(previous, start, end)

            for neighbor in graph.get_neighbors(current).keys():
                if neighbor not in visited:
                    stack.append(neighbor)
                    visited.add(neighbor)
                    previous[neighbor] = current
        return []

    def constructPath(self, previous: Dict[str, str], start: str, end: str) -> List[str]:
        path = []
        step = end

        while step is not None:
            path.append(step)
            step = previous.get(step)

        path.reverse()

        pathWithNames = [self.stopIdToName.get(stopId, stopId) for stopId in path]
        return pathWithNames

    def findClosestStop(self, stops: Dict[str, 'MetroStop'], latitude: float, longitude: float, tolerance: float) -> 'MetroStop':
        closestStop = None
        closestDistance = float('inf')

        for stop in stops.values():
            distance = self.calculateDistance(latitude, longitude, stop.getLatitude(), stop.getLongitude())
            if distance < closestDistance and distance <= tolerance:
                closestDistance = distance
                closestStop = stop
        return closestStop

    def calculateDistance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        # Haversine formula to calculate distance between two points on the Earth
        EARTH_RADIUS = 6371  # Radius of the Earth in kilometers

        latDistance = math.radians(lat2 - lat1)
        lonDistance = math.radians(lon2 - lon1)
        a = math.sin(latDistance / 2) * math.sin(latDistance / 2) + \
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
            math.sin(lonDistance / 2) * math.sin(lonDistance / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return EARTH_RADIUS * c  # Distance in kilometers

    def groupShapesById(self, shapes: Dict[str, 'MetroShape']) -> Dict[str, List['MetroShape']]:
        shapeGroups = {}
        for shape in shapes.values():
            shapeGroups.setdefault(shape.getShapeId(), []).append(shape)
        return shapeGroups
