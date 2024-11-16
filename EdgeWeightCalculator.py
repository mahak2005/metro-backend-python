class EdgeWeightCalculator:

    @staticmethod
    def calculateTravelTime(arrivalTime1, departureTime2):
        # Assuming time format is "HH:mm:ss"
        arrivalMillis = EdgeWeightCalculator.parseTimeToMillis(arrivalTime1)
        departureMillis = EdgeWeightCalculator.parseTimeToMillis(departureTime2)
        return (departureMillis - arrivalMillis) / 1000.0 / 60.0  # Convert to minutes

    @staticmethod
    def parseTimeToMillis(time):
        parts = time.split(":")
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])
        return (hours * 3600 + minutes * 60 + seconds) * 1000

    @staticmethod
    def calculateStopTime(arrivalTime, departureTime):
        arrivalMillis = EdgeWeightCalculator.parseTimeToMillis(arrivalTime)
        departureMillis = EdgeWeightCalculator.parseTimeToMillis(departureTime)
        return (departureMillis - arrivalMillis) / 1000.0 / 60.0  # Convert to minutes

    @staticmethod
    def getEdgeWeight(stopTimes, fromStopId, toStopId):
        # Assuming stopTimes is sorted by tripId and stop_sequence
        for stopTime in stopTimes.values():
            if stopTime.getStopId() == fromStopId:
                arrivalTime = stopTime.getArrivalTime()
                departureTime = stopTime.getDepartureTime()
                # Find the next stop in the sequence
                nextStopTime = EdgeWeightCalculator.findNextStopTime(stopTimes, stopTime.getTripId(), stopTime.getStopSequence())
                if nextStopTime is not None and nextStopTime.getStopId() == toStopId:
                    travelTime = EdgeWeightCalculator.calculateTravelTime(arrivalTime, nextStopTime.getArrivalTime())
                    stopTimeAtFromStop = EdgeWeightCalculator.calculateStopTime(arrivalTime, departureTime)
                    return travelTime + stopTimeAtFromStop
        return float('inf')  # No path found

    @staticmethod
    def findNextStopTime(stopTimes, tripId, currentStopSequence):
        for stopTime in stopTimes.values():
            if stopTime.getTripId() == tripId and stopTime.getStopSequence() == currentStopSequence + 1:
                return stopTime
        return None
