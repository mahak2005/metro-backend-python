class MetroTrip:
    def __init__(self, route_id, service_id, trip_id, shape_id):
        self.route_id = route_id
        self.service_id = service_id
        self.trip_id = trip_id
        self.shape_id = shape_id

    # Getters and setters
    def get_route_id(self):
        return self.route_id

    def set_route_id(self, route_id):
        self.route_id = route_id

    def get_service_id(self):
        return self.service_id

    def set_service_id(self, service_id):
        self.service_id = service_id

    def get_trip_id(self):
        return self.trip_id

    def set_trip_id(self, trip_id):
        self.trip_id = trip_id

    def get_shape_id(self):
        return self.shape_id

    def set_shape_id(self, shape_id):
        self.shape_id = shape_id

    def __str__(self):
        return (f"MetroTrip(routeId='{self.route_id}', serviceId='{self.service_id}', "
                f"tripId='{self.trip_id}', shapeId='{self.shape_id}')")
