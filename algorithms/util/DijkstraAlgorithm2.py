from collections import deque
from datetime import datetime
from util.DijkstraAlgorithm import DijkstraAlgorithm
from datetime import datetime
class DijkstraAlgorithm2:
    TIME_FORMATTER = "%H:%M:%S"
    MAX_EDGE_WEIGHT = 1.7976931348623157E308
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
        priorityQueue.append((0.0, startStopId))

        while priorityQueue:
            currentDistance, currentStopId = priorityQueue.pop(0)

            if currentStopId in visited:
                continue
            visited.add(currentStopId)

            # Process each neighbor
            for neighborStopId, travelTime in graph.get_neighbors(currentStopId).items():
                # Compute edge weight (travelTime + stopTime at the current stop)
                edgeWeight = travelTime + self.getStopTime(stopTimes, currentStopId)
                newDist = currentDistance + edgeWeight

                if newDist < distances[neighborStopId]:
                    distances[neighborStopId] = newDist
                    DijkstraAlgorithm.previousStops[neighborStopId] = currentStopId
                    priorityQueue.append((newDist, neighborStopId))
            # for neighborStopId, travelTime in graph.get_neighbors(currentStopId).items():
            #     edgeWeight = travelTime + self.getStopTime(stopTimes, currentStopId)
            #     newDist = currentDistance + edgeWeight
            #     print(f"Processing {currentStopId} -> {neighborStopId}: edgeWeight={edgeWeight}, newDist={newDist}")
            #     if newDist < distances[neighborStopId]:
            #         distances[neighborStopId] = newDist
            #         DijkstraAlgorithm.previousStops[neighborStopId] = currentStopId
            #         priorityQueue.append((newDist, neighborStopId))
        return distances

    def getStopTime(self, stopTimes, stopId):
        totalStopTime = 0.0
        for stopTimeData in stopTimes.values():
            if stopTimeData.getStopId() == stopId:
                try:
                    arrival_time_str = str(stopTimeData.getArrivalTime())
                    departure_time_str = str(stopTimeData.getDepartureTime())
                    arrival = datetime.strptime(arrival_time_str, DijkstraAlgorithm2.TIME_FORMATTER).time()
                    departure = datetime.strptime(departure_time_str, DijkstraAlgorithm2.TIME_FORMATTER).time()

                    arrival_minutes = arrival.hour * 60 + arrival.minute + arrival.second / 60
                    departure_minutes = departure.hour * 60 + departure.minute + departure.second / 60
                    duration_minutes = departure_minutes - arrival_minutes

                    if duration_minutes > 0:
                        totalStopTime += duration_minutes  # Add to total stop time
                except ValueError as e:
                    print(f"Error parsing time for stop ID {stopId}: {e}")
        return totalStopTime


    def getPath(self, endStopId):
        path = []
        step = endStopId

        while step is not None:
            path.insert(0, step)  
            step = DijkstraAlgorithm.previousStops.get(step)

        return path

    # Helper class to store stop and distance
    class StopDistance:
        def __init__(self, stopId, distance):
            self.stopId = stopId
            self.distance = distance

        def getStopId(self):
            return self.stopId

        def getDistance(self):
            return self.distance


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
