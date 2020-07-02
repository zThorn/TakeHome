class Stop:
    def __init__(self, stop_name: str, connections: list[str]):
        self.Name = stop_name
        self.Connections = connections

    #stop1.isConnection(stop2)
    def isConnection(self, target):
        return self.Name in target.Connections

