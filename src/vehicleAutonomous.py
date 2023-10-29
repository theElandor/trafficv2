import abc
from src.vehicleAbstract import VehicleAbstract
from src.utils import *

class VehicleAutonomous(VehicleAbstract):
    
    @abc.abstractmethod
    def action(self):
        return