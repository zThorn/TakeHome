from collections import namedtuple
from src.ingest.MBTAMarshaller import MBTAMarshaller
import click

@click.group()
def cli():
    pass

@cli.command("q1")
@click.option('--use-cache', default=False, help='Use the local json files to build the map')
def question_one(use_cache: bool):
    route_map = MBTAMarshaller().build_route_map(use_cache)
    #Question 1
    print("########## QUESTION 1 ##########")
    for line_id, line_name in route_map.get_lines():
        print(line_name)

@cli.command("q2")
@click.option('--use-cache', default=False, help='Use the local json files to build the map')
def question_two(use_cache: bool):
    route_map = MBTAMarshaller().build_route_map(use_cache)
    RouteResult = namedtuple('RouteLengthResult', ['RouteName', 'RouteLength'])
    max_route = RouteResult('', 0)
    min_route = RouteResult('', float("inf"))

    for route in route_map.get_routes():
        if len(route.stops) > max_route.RouteLength:
            max_route = RouteResult(route.route_name, len(route))
        elif len(route.stops) < min_route.RouteLength:
            min_route = RouteResult(route.route_name, len(route))

    print("########## QUESTION 2 pt 1. ##########")
    print("The max_route was : {0} with {1} stops".format(max_route.RouteName, max_route.RouteLength))
    print("########## QUESTION 2 pt 2. ##########")
    print("The min_route was : {0} with {1} stops".format(min_route.RouteName, min_route.RouteLength))

    print("########## QUESTION 2 pt 3. ##########")
    for stop in route_map.get_stops():
        if len(stop.lines) > 1:
            print("Stop {0} is on the following lines: {1} for a total of {2} lines".format(stop.name, ", ".join(stop.lines),len(stop.lines)))

@cli.command('route')
@click.option('--origin', help='The originating station')
@click.option('--destination', help='The destination station')
@click.option('--use-cache', default=False, help='Use the local json files to build the map')
def route_between(origin: str, destination: str, use_cache: bool):
    route_map = MBTAMarshaller().build_route_map(cached=use_cache)
    print(route_map.get_route_between_stops(route_map.get_stop(origin.lower()), route_map.get_stop(destination.lower())))

if __name__=='__main__':
    cli()