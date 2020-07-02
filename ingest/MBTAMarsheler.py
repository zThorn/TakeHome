import requests
import models.Map
from models.Route import Route

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
class MBTAMarsheler:
    base_api_route = "https://api-v3.mbta.com"
    mbta_route = base_api_route + "/routes?filter[type]=0,1"

    #This will be constructed later when we go to parse stops
    mbta_stops = base_api_route + "/stops?filter[route]={0}"

    def __init__(self):
        self.map = models.Map.Map()
        self.parseRoutes()
        self.parseStops()

    def getMap(self):
        return self.map

    def parseRoutes(self):
        raw = requests.get(self.mbta_route).json()
        for route in raw['data']:
            self.map.addLine(route['id'], route['attributes']['long_name'])

    def parseStops(self):
        for route_id, route_name in self.map.getLines():
            raw = requests.get(self.mbta_stops.format(route_id)).json()

            route_set = set()
            for stop in raw['data']:
                route_set.add(stop['attributes']['name'])
            r = Route(route_name, route_set)
            self.map.addRoute(r)

    def buildMap(self):
        raise NotImplementedError
