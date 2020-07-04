import requests
from src.models import Route
from src.models import Stop
from src.models import Map

'''
This class acts as an interface between the MBTA API => my object model
Ideally, any form of modifications required should be handled at this stage,
should be used something like this

s = MBTAMarsheller()
#Should handle building out the object model,
#From this point onwards, API/MBTA specific things should be fully out of the equation
#This way, if I needed to add a new transit line, its pretty much just a matter of creating a single class here
map = MBTAMarsheller().buildMap()

map.getMaxStops()
map.getRouteBetween("Park St", "North Station")

'''
class MBTAMarsheller:
    base_api_route = "https://api-v3.mbta.com"
    mbta_route = base_api_route + "/routes?filter[type]=0,1"

    #This will be constructed later when we go to parse stops
    mbta_stops = base_api_route + "/stops?filter[route]={0}"

    def __init__(self):
        self.map = Map()


    def buildMap(self) -> Map:
        route_json = self.getRouteJSON()

        self.getRouteDefinitions(route_json)
        self.parseRouteDetails()
        self.parseEdges()
        return self.map

    def getMap(self) -> Map:
        return self.map

    def getRouteJSON(self) -> dict:
        return requests.get(self.mbta_route).json()

    def getStopJSON(self, route_id: str) -> dict:
        return requests.get(self.mbta_stops.format(route_id)).json()

    def getRouteDefinitions(self, raw: dict) -> None:
        for route in raw['data']:
            self.map.add_line_mapping(route['id'], route['attributes']['long_name'])

    def parseRouteDetails(self) -> None:
        for route_id, route_name in self.map.getLines():
            stops = self.getStopJSON(route_id)
            self.marshalStopsIntoRoutes(route_name, stops)


    def marshalStopsIntoRoutes(self, route_name: str, stops: dict):
        route_stops = []
        for stop in stops['data']:
            stop_name = stop['attributes']['name']
            s = Stop(stop_name, route_name)
            route_stops.append(s)
            self.map.addStop(s)
        r = Route(route_name, route_stops)
        self.map.addRoute(r)

    #I have a list that looks like this:
    #[Red Line, Green Line B, Green Line C, Green Line D, Green Line E]
    #For each node, I need to add an edge to the appropriate graph
    def parseEdges(self) -> None:
        for stop in self.map.get_stops():
            if len(stop.lines) > 1:
                for i in stop.lines:
                    self.map.add_transfer_routes(i, stop.lines)
