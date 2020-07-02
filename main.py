from collections import namedtuple
import ingest.MBTAMarsheler as MBTA

map = MBTA.MBTAMarsheler().getMap()
RouteResult = namedtuple('RouteLengthResult',['RouteName', 'RouteLength'])

#Question 1
print("########## QUESTION 1 ##########")
for line_id, line_name in map.getLines():
    print(line_name)


#Question 2
maxRoute = RouteResult('', 0)
minRoute = RouteResult('', float("inf"))

for route in map.getRoutes():
    if len(route.stops) > maxRoute.RouteLength:
        maxRoute = RouteResult(route.route_name, len(route.stops))
    elif len(route.stops) < minRoute.RouteLength:
        minRoute = RouteResult(route.route_name, len(route.stops))
print("########## QUESTION 2 ##########")
print(maxRoute)
print(minRoute)
