from src.utils import *
from src.crossroadsDict import CrossroadsDict

class Crossroad:
    name = ""
    in_edges = []
    position = []
    current_idle_time = 0

    def __init__(self, name, in_edges, position):
        self.name = name
        self.in_edges = in_edges
        self.position = position
        CrossroadsDict.addCrossroad(self)

    def getName(self):
        return self.name

    def getInEdges(self):
        return self.in_edges

    def getPosition(self):
        return self.position

    def setIdleTime(self):
        if self.current_idle_time == 0:
            self.current_idle_time = traci.simulation.getTime()

    def resetIdleTime(self):
        self.current_idle_time = 0

    def getIdleTime(self):
        if self.current_idle_time != 0:
            time_passed = traci.simulation.getTime() - self.current_idle_time
            return time_passed
        return 0

    def __str__(self):
        return self.name
