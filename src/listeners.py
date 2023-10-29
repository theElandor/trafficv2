import traci
from src.utils import *

from src.vehiclesDict import VehiclesDict

class Listener(traci.StepListener):

    def __init__(self, step_limit, settings, routes, crossroads_names):
        # When listener is initialized, vehicles have yet been spawned, with one simulation step for each of them
        self.step_count = len(VehiclesDict.vd.keys())
        self.step_limit = step_limit
        self.simulation_status = True
        self.settings = settings
        self.routes = routes
        self.crossroads_names = crossroads_names

    # NOTE: step method wants argument 't'
    def step(self, t):
        """
        At each traci.simulationStep() invocation, this method is invoked to execute a 
        routine to check step limit, apply common operations (i.e. rerouting check 
        of vehicles) and specific operations for models (i.e. 'Hurry' changing in 
        'Emergent Behavior' model.
        """
        # UNCOMMENT to gather data at each timestamp
        self.step_count += 1
        if self.step_limit != 0 and self.step_count >= self.step_limit:
            self.simulation_status = False
            return False

        for v in VehiclesDict.vd.values():
            # print("reroute\n")
            v.reroute()
            v.setLabel()

        # indicate that the step listener should stay active in the next step
        return True

    def getStep(self):
        return self.step_count

    def getSimulationStatus(self):
        return self.simulation_status

class AutonomousListener(Listener):
    def __init__(self, step_limit, settings):
        super().__init__(step_limit, settings)

    def step(self, t):
        super().step(t)

        for v in VehiclesDict.vd.values():
            v.action()

        return True
