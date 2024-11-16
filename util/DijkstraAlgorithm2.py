from collections import deque
from datetime import datetime
from util.DijkstraAlgorithm import DijkstraAlgorithm
class DijkstraAlgorithm2:
    TIME_FORMATTER = "%H:%M:%S"  # Equivalent to DateTimeFormatter in Java

    def dijkstra(self, graph, startStopId, stopTimes):
        # Initialize distance map and priority queue
        distances = {}
        priorityQueue = []
        visited = set()

        # Set initial distances to infinity and the start node to zero
        for stopId in graph.get_all_stops():
            distances[stopId] = float('inf')
            DijkstraAlgorithm.previousStops[stopId] = None
        distances[startStopId] = 0.0
        priorityQueue.append(StopDistance(startStopId, 0.0))

        while priorityQueue:
            current = min(priorityQueue, key=lambda x: x.distance)  # Get the stop with the smallest distance
            priorityQueue.remove(current)
            currentStopId = current.getStopId()

            if currentStopId in visited:
                continue
            visited.add(currentStopId)

            # Process each neighbor
            for neighborStopId, travelTime in graph.get_neighbors(currentStopId).items():
                # Compute edge weight (travelTime + stopTime at the current stop)
                edgeWeight = travelTime + self.getStopTime(stopTimes, currentStopId)
                newDist = distances[currentStopId] + edgeWeight

                if newDist < distances[neighborStopId]:
                    distances[neighborStopId] = newDist
                    DijkstraAlgorithm.previousStops[neighborStopId] = currentStopId
                    priorityQueue.append(StopDistance(neighborStopId, newDist))

        return distances

    def getStopTime(self, stopTimes, stopId):
        totalStopTime = 0.0
        for stopTimeData in stopTimes.values():
            if stopTimeData.getStopId() == stopId:
                try:
                    arrival = datetime.strptime(stopTimeData.getArrivalTime(), self.TIME_FORMATTER)
                    departure = datetime.strptime(stopTimeData.getDepartureTime(), self.TIME_FORMATTER)
                    duration = (departure - arrival).seconds / 60.0  # Convert duration to minutes
                    totalStopTime += duration
                except ValueError as e:
                    print(f"Error parsing time for stop ID {stopId}: {str(e)}")
        return totalStopTime

    def getPath(self, endStopId):
        path = deque()
        step = endStopId

        while step is not None:
            path.appendleft(step)  # Add elements at the front instead of reversing later
            step = DijkstraAlgorithm.previousStops.get(step)

        return list(path)  # Convert to List if needed

    # Helper class to store stop and distance
class StopDistance:
    def __init__(self, stopId, distance):
        self.stopId = stopId
        self.distance = distance

    def getStopId(self):
        return self.stopId

    def getDistance(self):
        return self.distance

    # To enable comparison of StopDistance objects based on distance for priority queue
    def __lt__(self, other):
        return self.distance < other.distance



# # Example of how to use DijkstraAlgorithm2
# if __name__ == "__main__":
#     graph = MetroGraph()  # Create a MetroGraph object
#     stop_times = {}  # Dictionary to hold MetroStopTime objects (key: stop_id)
#     dijkstra = DijkstraAlgorithm2()

#     # Run Dijkstra's algorithm from a start stop
#     start_stop_id = 'A'  # Example start stop
#     end_stop_id = 'D'    # Example end stop
#     distances = dijkstra.dijkstra(graph, start_stop_id, stop_times)
#     path = dijkstra.get_path(end_stop_id)

#     print(f"Shortest path from {start_stop_id} to {end_stop_id}: {path}")
#     print(f"Distances: {distances}")
