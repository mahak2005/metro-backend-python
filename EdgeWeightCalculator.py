from model.MetroStopTime import MetroStopTime
from util.DijkstraAlgorithm2 import DijkstraAlgorithm2
class EdgeWeightCalculator:
    @staticmethod
    def parseTimeToMillis(time: str) -> int:
        """Parse time in 'HH:mm:ss' format to milliseconds."""
        parts = list(map(int, time.split(":")))
        hours, minutes, seconds = parts
        return (hours * 3600 + minutes * 60 + seconds) * 1000

    @staticmethod
    def calculateTravelTime(arrivalTime1: str, departureTime2: str) -> float:
        """Calculate travel time in minutes."""
        arrivalMillis = EdgeWeightCalculator.parseTimeToMillis(arrivalTime1)
        departureMillis = EdgeWeightCalculator.parseTimeToMillis(departureTime2)
        # Ensure no negative time difference by checking the condition
        if departureMillis < arrivalMillis:
            return 0  # or handle differently if necessary
        return (departureMillis - arrivalMillis) / 1000.0 / 60.0

    @staticmethod
    def calculateStopTime(arrivalTime: str, departureTime: str) -> float:
        """Calculate stop time in minutes."""
        arrivalMillis = EdgeWeightCalculator.parseTimeToMillis(arrivalTime)
        departureMillis = EdgeWeightCalculator.parseTimeToMillis(departureTime)
        # Ensure no negative time difference by checking the condition
        if departureMillis < arrivalMillis:
            return 0  # or handle differently if necessary
        return (departureMillis - arrivalMillis) / 1000.0 / 60.0

    @staticmethod
    def findNextStopTime(stopTimes: dict, tripId: str, currentStopSequence: int) -> MetroStopTime:
        """Find the next stop time in the sequence."""
        for stopTime in stopTimes.values():
            if stopTime.getTripId() == tripId and stopTime.getStopSequence() == currentStopSequence + 1:
                return stopTime
        return None

    @staticmethod
    def getEdgeWeight(stopTimes: dict, fromStopId: str, toStopId: str) -> float:
        """Calculate the edge weight as the sum of travel time and stop time."""
        
        for stopTime in stopTimes.values():
            if stopTime.getStopId() == fromStopId:
                arrivalTime = stopTime.getArrivalTime()
                departureTime = stopTime.getDepartureTime()
                nextStopTime = EdgeWeightCalculator.findNextStopTime(
                    stopTimes, stopTime.getTripId(), stopTime.getStopSequence()
                )
                if nextStopTime and nextStopTime.getStopId() == toStopId:
                    travelTime = EdgeWeightCalculator.calculateTravelTime(arrivalTime, nextStopTime.getArrivalTime())
                    stopTimeAtFromStop = EdgeWeightCalculator.calculateStopTime(arrivalTime, departureTime)
                    return travelTime + stopTimeAtFromStop
        return DijkstraAlgorithm2.MAX_EDGE_WEIGHT  # No path found
