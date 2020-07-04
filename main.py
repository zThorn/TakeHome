from collections import namedtuple
import src.ingest.MBTAMarsheller as MBTA

map = MBTA.MBTAMarsheler().buildMap()
RouteResult = namedtuple('RouteLengthResult',['RouteName', 'RouteLength'])

#Question 1
print("########## QUESTION 1 ##########")
for line_id, line_name in map.getLines():
    print(line_name)


#Question 2
maxRoute = RouteResult('', 0)
minRoute = RouteResult('', float("inf"))

for route in map.get_routes():
    if len(route.stops) > maxRoute.RouteLength:
        maxRoute = RouteResult(route.route_name, len(route))
    elif len(route.stops) < minRoute.RouteLength:
        minRoute = RouteResult(route.route_name, len(route))

print("########## QUESTION 2 pt 1. ##########")
print(maxRoute)
print("########## QUESTION 2 pt 2. ##########")
print(minRoute)
print("########## QUESTION 2 pt 3. ##########")
for stop in map.get_stops():
    if len(stop.lines) > 1:
        print("Stop {0} is on the following lines: {1}".format(stop.name, ", ".join(stop.lines)))
print("done")
source = "Mattapan"
destination = "Wonderland"

print(map.getRouteBetweenStops(map.get_stop(source), map.get_stop(destination)))