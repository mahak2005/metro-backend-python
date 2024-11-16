class MetroStopTime:
    def __init__(self, tripId, arrivalTime, departureTime, stopId, stopSequence, shapeDistTraveled):
        self.tripId = tripId
        self.arrivalTime = arrivalTime
        self.departureTime = departureTime
        self.stopId = stopId
        self.stopSequence = stopSequence
        self.shapeDistTraveled = shapeDistTraveled

    # Getters and Setters
    def getTripId(self):
        return self.tripId

    def setTripId(self, tripId):
        self.tripId = tripId

    def getArrivalTime(self):
        return self.arrivalTime

    def setArrivalTime(self, arrivalTime):
        self.arrivalTime = arrivalTime

    def getDepartureTime(self):
        return self.departureTime

    def setDepartureTime(self, departureTime):
        self.departureTime = departureTime

    def getStopId(self):
        return self.stopId

    def setStopId(self, stopId):
        self.stopId = stopId

    def getStopSequence(self):
        return self.stopSequence

    def setStopSequence(self, stopSequence):
        self.stopSequence = stopSequence

    def getShapeDistTraveled(self):
        return self.shapeDistTraveled

    def setShapeDistTraveled(self, shapeDistTraveled):
        self.shapeDistTraveled = shapeDistTraveled

    def __str__(self):
        return f"MetroStopTime{{tripId='{self.tripId}', arrivalTime='{self.arrivalTime}', departureTime='{self.departureTime}', stopId='{self.stopId}', stopSequence={self.stopSequence}, distance={self.shapeDistTraveled}}}"
