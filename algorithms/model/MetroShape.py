class MetroShape:
    def __init__(self, shape_id, latitude, longitude, sequence, distance_traveled):
        self.shape_id = shape_id
        self.latitude = latitude
        self.longitude = longitude
        self.sequence = sequence
        self.distance_traveled = distance_traveled

    # Getter for shape_id
    def getShapeId(self):
        return self.shape_id

    # Getter for latitude
    def getLatitude(self):
        return self.latitude

    # Getter for longitude
    def getLongitude(self):
        return self.longitude

    # Getter for sequence
    def getSequence(self):
        return self.sequence

    # Getter for distance_traveled
    def get_distance_traveled(self):
        return self.distance_traveled

    def __str__(self):
        return f"MetroShape(shape_id='{self.shape_id}', latitude={self.latitude}, longitude={self.longitude}, sequence={self.sequence}, distance_traveled={self.distance_traveled})"
