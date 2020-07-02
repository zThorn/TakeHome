class Route:
    def __init__(self, route_name, stops):
        self.route_name = route_name
        self.stops = stops

    def __str__(self):
        return str("Route Name: "+self.route_name+" Stops: "+str(self.stops))
