'''
Static class containing a dictionary of crossroads
'''

class VehiclesDict():
    vd = {}

    def addVehicle(veh):
        VehiclesDict.vd[veh.getID()] = veh 
    
    def getVehicle(veh):
        return VehiclesDict.vd[veh]