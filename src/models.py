from collections import deque
from collections.abc import Iterable


class Route:
    def __init__(self, route_name: str, stops: list) -> None:
        self.route_name = route_name
        self.stops = stops

    def __len__(self) -> int:
        return len(self.stops)

    def __str__(self) -> str:
        return "Route Name: {0} Stops: {1}".format(self.route_name, self.stops)


class Stop:
    def __init__(self,stop_id: str, stop_name: str, line: str) -> None:
        self.name = stop_name
        self.id = stop_id
        self.lines = [line]

    def __str__(self) -> str:
        return "Stop: {0} Routes: {1}".format(self.name, self.lines)

    def add_line(self, line) -> None:
        self.lines.append(line[0])


class RouteMap:
    def __init__(self):
        self.lines = {}
        self.routes = []
        self.stops = {}
        self.transfer_routes = {}

    def add_line_mapping(self, line_id: str, line_name: str) -> None:
        self.lines[line_id] = line_name

    def add_route(self, route: Route) -> None:
        """
        :param route: A constructed route object
        :return: None

        Method is used to automatically add a route object to both the overall route list, as well as to instantiate
        a dict of RouteNames -> possible switches
        """
        self.routes.append(route)
        self.transfer_routes[route.route_name] = set()

    def add_transfer_routes(self, origin_route: str, all_available_routes: list) -> None:
        """
        :param origin_route: The originating route, this will be treated as the key
        :param all_available_routes: All stops that are possible to be switched to from the originating_route
        :return: None
        """

        # We clone, and then remove the originating stop, so that there isn't a situation where a route
        # maps to itself
        available_routes = all_available_routes.copy()
        available_routes.remove(origin_route)
        self.transfer_routes[origin_route].update(set(available_routes))

    def get_routes(self) -> list:
        return self.routes

    def get_lines(self) -> Iterable:
        return self.lines.items()

    def get_stop(self, stop_name: str) -> Stop:
        return self.stops[stop_name]

    def get_stops(self) -> Iterable:
        return self.stops.values()

    def add_stop(self, stop: Stop) -> None:
        """
        :param stop: A stop object representing a new, or pre-existing line.  In the event that the stop has already
                     been registered, it's assumed that this is an additional line that is possible
                     to be travelled down.
        :return:
        """
        # This is a transition stop, which signifies a connection between two lines
        # Add this to my edge graph
        if stop.name in self.stops and stop.id == self.stops[stop.name].id:
            self.stops[stop.name].add_line(stop.lines)

        # This is a work around to handle st paul street specifically.  There's no real way of handling the input
        # in question 3 so that it deterministically resolves this appropriately.
        elif stop.name in self.stops and stop.id != self.stops[stop.name].id:
            self.stops[stop.name+stop.id] = stop
        else:
            self.stops[stop.name] = stop

    def get_route_between_stops(self, starting_stop: Stop, destination: Stop) -> list:
        """
        :param starting_stop: A stop object representing the originating station.  Can easily be gotten using
                                `get_stop` in combination with a string representation
        :param destination: A stop object representing the originating station.  Can easily be gotten using
                                `get_stop` in combination with a string representation
        :return: None

        This method is an implementation of a BFS with an early escape in the event that 2 stops are already on the
        same line, or an intersection is possible.
        """
        # Check for all routes attached to both stops if there exists an intersection
        intersecting_lines = set(starting_stop.lines).intersection(set(destination.lines))
        if intersecting_lines:
            return [intersecting_lines.pop()]

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
