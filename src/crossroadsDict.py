'''
Static class containing a dictionary of crossroads
'''

class CrossroadsDict():
    cl = {}
    global_in_edges = []

    def addCrossroad(cross):
        CrossroadsDict.cl[cross.getName()] = cross 
        CrossroadsDict.global_in_edges += cross.getInEdges()
    
    def getCrossroad(cross):
        return CrossroadsDict.cl[cross]

    def getGlobalInEdges():
        return CrossroadsDict.global_in_edges