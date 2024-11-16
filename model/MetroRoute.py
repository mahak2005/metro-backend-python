class MetroRoute:
    def __init__(self, route_id, route_short_name, route_long_name, route_color):
        self.route_id = route_id
        self.route_short_name = route_short_name
        self.route_long_name = route_long_name
        self.route_color = route_color

    # Getters and Setters
    def get_route_id(self):
        return self.route_id

    def set_route_id(self, route_id):
        self.route_id = route_id

    def get_route_short_name(self):
        return self.route_short_name

    def set_route_short_name(self, route_short_name):
        self.route_short_name = route_short_name

    def get_route_long_name(self):
        return self.route_long_name

    def set_route_long_name(self, route_long_name):
        self.route_long_name = route_long_name

    def get_route_color(self):
        return self.route_color

    def set_route_color(self, route_color):
        self.route_color = route_color

    def __str__(self):
        return f"MetroRoute(route_id='{self.route_id}', short_name='{self.route_short_name}', long_name='{self.route_long_name}', color='{self.route_color}')"
