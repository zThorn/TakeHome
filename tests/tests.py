import unittest


class TestMBTAMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        from src.ingest.MBTAMarshaller import MBTAMarshaller
        cls.cached_route_map = MBTAMarshaller().build_route_map(cached=True)
        cls.route_map = MBTAMarshaller().build_route_map(cached=False)


    def testAddLineStops(self):
        from src.models import Stop
        s1 = Stop("UniqParkId","Park Street", "Red Line")
        s1.add_line(["Green Line B"])
        s1.add_line(["Green Line C"])
        s1.add_line(["Green Line D"])
        self.assertEqual(s1.lines, ['Red Line', 'Green Line B', 'Green Line C', 'Green Line D'])

    def testRouteParse(self):
        self.assertEqual(len(self.cached_route_map.lines), 8)
        self.assertIn("Red", self.cached_route_map.lines.keys())
        self.assertEqual(self.cached_route_map.lines["Red"], "Red Line")
        self.assertEqual(len(self.cached_route_map.lines), 8)
        self.assertIn("Red", self.cached_route_map.lines.keys())
        self.assertEqual(self.cached_route_map.lines["Red"], "Red Line")

    def testGetRouteBetweenStopsDifferentLines(self):
        self.assertEqual(self.cached_route_map.get_route_between_stops(self.cached_route_map.get_stop("aquarium"),
                                                                       self.cached_route_map.get_stop(
                                                                           "downtown crossing")),
                         ['Blue Line', 'Orange Line'])

        self.assertEqual(self.route_map.get_route_between_stops(self.route_map.get_stop("aquarium"),
                                                                self.route_map.get_stop("downtown crossing")),
                         ['Blue Line', 'Orange Line'])

    def testGetRouteBetweenStopsSameLine(self):
        self.assertEqual(self.cached_route_map.get_route_between_stops(self.cached_route_map.get_stop("aquarium"),
                                                                       self.cached_route_map.get_stop("state")),
                         ['Blue Line'])

        self.assertEqual(self.route_map.get_route_between_stops(self.route_map.get_stop("aquarium"),
                                                                self.route_map.get_stop("state")),
                         ['Blue Line'])

    def testParseStPaulStreet(self):
        self.assertEqual(len(self.cached_route_map.get_stop("saint paul street").lines), 1)
        self.assertEqual(len(self.route_map.get_stop("saint paul street").lines), 1)

    def testGetMinStopNum(self):
        from collections import namedtuple

        RouteResult = namedtuple('RouteLengthResult', ['RouteName', 'RouteLength'])
        max_route = RouteResult('', 0)
        min_route = RouteResult('', float("inf"))

        for route in self.route_map.get_routes():
            if len(route.stops) > max_route.RouteLength:
                max_route = RouteResult(route.route_name, len(route))
            elif len(route.stops) < min_route.RouteLength:
                min_route = RouteResult(route.route_name, len(route))

        cached_max_route = RouteResult('', 0)
        cached_min_route = RouteResult('', float("inf"))

        for route in self.cached_route_map.get_routes():
            if len(route.stops) > cached_max_route.RouteLength:
                cached_max_route = RouteResult(route.route_name, len(route))
            elif len(route.stops) < cached_min_route.RouteLength:
                cached_min_route = RouteResult(route.route_name, len(route))

        self.assertEqual(max_route.RouteLength, 24)
        self.assertEqual(min_route.RouteLength, 8)
        self.assertEqual(cached_max_route.RouteLength, 24)
        self.assertEqual(cached_min_route.RouteLength, 8)

if __name__ == '__main__':
    unittest.main()
