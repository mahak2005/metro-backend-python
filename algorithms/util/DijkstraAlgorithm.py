import heapq

class DijkstraAlgorithm:

    previousStops = {}

    def dijkstra(self, graph, startStopId):
        # Priority queue to select the stop with the smallest distance
        priorityQueue = []
        distances = {}
        visited = set()

        # Initialize distances and priority queue
        for stopId in graph.get_all_stops():
            distances[stopId] = float('inf')
            self.previousStops[stopId] = None
        distances[startStopId] = 0.0
        heapq.heappush(priorityQueue, StopDistance(startStopId, 0.0))

        while priorityQueue:
            currentStopDistance = heapq.heappop(priorityQueue)
            currentStopId = currentStopDistance.getStopId()

            if currentStopId in visited:
                continue
            visited.add(currentStopId)

            for neighborEntry in graph.get_neighbors(currentStopId).items():
                neighborStopId = neighborEntry[0]
                weight = neighborEntry[1]
                newDist = distances[currentStopId] + weight

                if newDist < distances[neighborStopId]:
                    distances[neighborStopId] = newDist
                    self.previousStops[neighborStopId] = currentStopId
                    heapq.heappush(priorityQueue, StopDistance(neighborStopId, newDist))

        return distances

    def getPath(self, endStopId, previousStops):
        path = []
        at = endStopId
        while at is not None:
            path.append(at)
            at = previousStops.get(at)
        path.reverse()
        return path

    # Inner class to represent a stop and its distance
class StopDistance:
    def __init__(self, stopId, distance):
        self.stopId = stopId
        self.distance = distance

    def getStopId(self):
        return self.stopId

    def getDistance(self):
        return self.distance

    # For heapq to work with StopDistance objects, we need comparison logic
    def __lt__(self, other):
        return self.distance < other.distance



# Example of how to use DijkstraAlgorithm
# if __name__ == "__main__":
#     # Assuming the `MetroGraph` and `MetroStop` have the appropriate methods as needed
#     graph = MetroGraph()  # Create a MetroGraph object
#     dijkstra = DijkstraAlgorithm()

#     # Run Dijkstra's algorithm from a start stop
#     start_stop_id = 'A'  # Example start stop
#     end_stop_id = 'D'    # Example end stop
#     distances = dijkstra.dijkstra(graph, start_stop_id)
#     path = dijkstra.get_path(end_stop_id)

#     print(f"Shortest path from {start_stop_id} to {end_stop_id}: {path}")
#     print(f"Distances: {distances}")
