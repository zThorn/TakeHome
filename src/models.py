from collections import deque
from collections.abc import Iterable


class Route:
    def __init__(self, route_name: str, stops: list) -> None:
        self.route_name = route_name
        self.stops = stops

    def __len__(self) -> int:
        return len(self.stops)

    def __str__(self) -> str:
        return str("Route Name: "+self.route_name+" Stops: "+str(self.stops))


class Stop:
    def __init__(self, stop_name: str, line: str) -> None:
        self.name = stop_name
        self.lines = [line]

    def add_line(self, line) -> None:
        self.lines.append(line[0])


class Map:
    def __init__(self):
        '''
          This represents unique LINES, and is in the format
          Source_name => destn names
          For the MBTA, this might look like
          ["Red_Line" : ["Green_Line", "Orange_Line"]},
          {"Green_Line" : ["Red_Line"]},]

          This is a single to many list that represents all possible routes a given stop could go to
          Example of a single complex entry might look like this:

            {"Park_Street" : ["Govt Center", "Charles/MGH", "Downtown Crossing", "Boylston"]
            OR
            Could do it to map a single stop => connecting lines, null if none, which would make the 2nd question effectively immediately answerable
            {"Park_Street" : ["Green_Line", "Red_Line"]

            OR
            Do a map of stop objects to stop objects, and just force an iteration over to get the connecting lines

        '''
        self.lines = dict()
        self.routes = []
        self.stops = {}
        self.transfer_routes = {}

    def add_line_mapping(self, line_id: str, line_name: str) -> None:
        self.lines[line_id] = line_name

    def addRoute(self, route: Route) -> None:
        self.routes.append(route)
        self.transfer_routes[route.route_name] = set()

    def add_transfer_routes(self, origin_route, all_available_routes) -> None:
        '''
        :param origin_route: The originating stop, this will
        :param all_available_routes: all stops that are possible to be switched to from the origin
        :return: None
        '''

        # We clone, and then remove the originating stop, so that
        available_routes = all_available_routes.copy()
        available_routes.remove(origin_route)

        self.transfer_routes[origin_route].update(set(available_routes))

    def get_routes(self) -> list:
        return self.routes

    def getLines(self) -> Iterable:
        return self.lines.items()

    def get_stop(self, stopName: str) -> Stop:
        return self.stops[stopName]

    def get_stops(self) -> Iterable:
        return self.stops.values()

    # Contains dict of stop_names => stop_objects
    def addStop(self, stop: Stop) -> None:
        # This is a transition stop, which signifies an edge connection between two lines
        # Add this to my edge graph
        if stop.name in self.stops:
            self.stops[stop.name].add_line(stop.lines)
        else:
            self.stops[stop.name] = stop

    # This should be called on 2 stop objects
    def getRouteBetweenStops(self, starting_stop: Stop, destination: Stop) -> list:

        # Check for all routes attached to both stops if there exists an intersection
        intersecting_lines = set(starting_stop.lines).intersection(set(destination.lines))
        if intersecting_lines:
            return intersecting_lines.pop()

        queue = deque()
        queue.append([starting_stop.lines[0]])

        while queue:
            path = queue.popleft()
            node = path[-1]

            if node in destination.lines:
                return path

            for adjacent in self.transfer_routes.get(node):
                new_path = list(path)
                new_path.append(adjacent)
                queue.append(new_path)




