import json
import requests
from config import ROOT_DIR
from src.models import Route
from src.models import Stop
from src.models import RouteMap


class MBTAMarshaller:
    """
    This class acts as an interface between the MBTA API => my object model
    Ideally, any form of modifications to the underlying data should be handled at this stage,
    and any additional transit lines being added should mirror this pattern.

    For Question 1:
        I've opted to shift the filtering off to the API.  Typically, I evaluate whether or not to use
        API specific features based on their likelihood of deprecation, as well as the difficulty of migrating away
        from said features.  Generally, if I believe there's moderate or greater risk that the feature could go away,
        and the feature or filter isn't too hard to implement myself, I would do so.  In this case, I thought
        the filter would be pretty trivial to implement locally if need be, but was also
        pretty unlikely to be removed from the MBTA's API (It seems pretty core).  So due to that, I opted to use
        the MBTA's compute power, instead of my own!

    """

    base_api_route = "https://api-v3.mbta.com"
    mbta_route_api = base_api_route + "/routes?filter[type]=0,1"
    mbta_stops_api = base_api_route + "/stops?filter[route]={0}"
    cached_json_loc = ROOT_DIR + "/data/"

    def __init__(self):
        self.route_map = RouteMap()

    def build_route_map(self, cached=False) -> RouteMap:
        route_json = self.get_route_json(cached)
        self.get_route_definitions(route_json)
        self.parse_route_details(cached)
        self.parse_intersections()

        return self.route_map

    def get_route_map(self) -> RouteMap:
        return self.route_map

    def get_route_json(self, cached: bool) -> dict:
        if cached:
            with open(self.cached_json_loc + "Route.json") as f:
                return json.load(f)
        else:
            return requests.get(self.mbta_route_api).json()

    def get_stop_json(self, route_id: str, cached: bool) -> dict:
        if cached:
            with open(self.cached_json_loc + route_id + ".json") as f:
                return json.load(f)
        else:
            return requests.get(self.mbta_stops_api.format(route_id)).json()

    def get_route_definitions(self, route_json: dict) -> None:
        """
        :param route_json: A dict containing raw route level data from the /routes endpoint
        :return: None

        For Each route definition within the provided dict, generate a route_id -> long form object
        """
        for route in route_json['data']:
            self.route_map.add_line_mapping(route['id'], route['attributes']['long_name'])

    def parse_route_details(self, cached=False) -> None:
        """
        :param cached: Boolean, determines whether or not to use locally saved versions of requests,
                       or to hit the server
        :return: None

        For each route that's been registered, make an API call to get a JSON object of all stops registered to
        that route.  Afterwards, marshal all of the stops into route object, and the overall dict of stops

        """
        for route_id, route_name in self.route_map.get_lines():
            stops = self.get_stop_json(route_id, cached)
            self.marshal_stops_into_routes(route_name, stops)

    def marshal_stops_into_routes(self, route_name: str, stops: dict) -> None:
        """
        :param route_name:
        :param stops: A parsed json dict containing stop level data
        :return:

        Iterates over all stops in the provided stops dict,
        and creates all of the appropriate stop objects.
        These objects are used to create the appropriate Route object,
        and will then be added to the overall map
        object on completion.
        """
        route_stops = []
        for stop in stops['data']:
            stop_name = stop['attributes']['name'].lower()
            stop_id = stop['id']
            s = Stop(stop_id, stop_name, route_name)
            route_stops.append(s)
            self.route_map.add_stop(s)

        self.route_map.add_route(Route(route_name, route_stops))

    def parse_intersections(self) -> None:
        """
        :return:
            Iterate over every stop, and build a dictionary from each of
            the stops available lines -> all the other lines that were found.
            This is just effectively building a graph between all lines
        """
        for stop in self.route_map.get_stops():
            # If the given stop has multiple lines associated with it, it must be a transfer point
            if len(stop.lines) > 1:
                for i in stop.lines:
                    self.route_map.add_transfer_routes(i, stop.lines)
