from models.Route import Route


class Map:

    def __init__(self):
        #This represents unique LINES, and is in the format
        #Source_name => destn names
        #For the MBTA, this might look like
        # ["Red_Line" : ["Green_Line", "Orange_Line"]},
        # {"Green_Line" : ["Red_Line"]},]
        #self.connections = list

        #A set of lines
        self.lines = dict()
        #This is a single to many list that represents all possible routes a given stop could go to
        #Example of a single complex entry might look like this:
        '''
            {"Park_Street" : ["Govt Center", "Charles/MGH", "Downtown Crossing", "Boylston"]      
        
        
        '''
        self.routes = []
        self.stops = {}



    def addLine(self, id, lineName):
        self.lines[id] = lineName

    def addRoute(self, route):
        self.routes.append(route)

    def getRoutes(self):
        return self.routes

    def getLines(self):
        return self.lines.items()

    def addStop(self, stop):
        raise NotImplementedError
