class Graph():
    def __init__(self, connections): #connections = [[A,B],[B,C], ...]
        self.connections = {}
        for conn in connections:
            self.connections[conn[0]] = []            
        for conn in connections:
            self.connections[conn[0]].append('edge'+str(conn[1])+'-'+str(conn[0])+'_0')
    def printGraph(self):
        for c in self.connections:
            print(c + " " + str(self.connections[c]))
    def __str__(self):
        return str(self.connections)
