class MetroStop:
    def __init__(self, stop_id, stop_name, latitude, longitude):
        self.stop_id = stop_id
        self.stop_name = stop_name
        self.latitude = latitude
        self.longitude = longitude
        self.distance = 0.0  # Default distance value

    # Getters and setters
    def get_distance(self):
        return self.distance

    def set_distance(self, distance):
        self.distance = distance

    def getStopId(self):
        return self.stop_id

    def set_stop_id(self, stop_id):
        self.stop_id = stop_id

    def getStopName(self):
        return self.stop_name

    def set_stop_name(self, stop_name):
        self.stop_name = stop_name

    def getLatitude(self):
        return self.latitude

    def set_latitude(self, latitude):
        self.latitude = latitude

    def getLongitude(self):
        return self.longitude

    def set_longitude(self, longitude):
        self.longitude = longitude

    def __str__(self):
        return f"MetroStop(id='{self.stop_id}', name='{self.stop_name}', latitude={self.latitude}, longitude={self.longitude})"
