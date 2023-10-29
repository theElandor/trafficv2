from collections import defaultdict
class OrderedEdges:
    def __init__(self):
        self.in_edges = defaultdict()
        self.fillDict()
    def fillDict(self):
        self.in_edges['A'] = ['edgeB-A', 'edge2-A','edge6-A','edgeD-A']
        self.in_edges['B'] = ['edgeC-B', 'edge3-B','edgeA-B','edgeE-B']
        self.in_edges['C'] = ['edge10-C', 'edge4-C','edgeB-C','edgeF-C']
        self.in_edges['D'] = ['edgeE-D', 'edgeA-D','edge11-D','edgeG-D']
        self.in_edges['E'] = ['edgeF-E', 'edgeB-E','edgeD-E','edgeH-E']
        self.in_edges['F'] = ['edge15-F', 'edgeC-F','edgeE-F','edgeI-F']
        self.in_edges['G'] = ['edgeH-G', 'edgeD-G','edge16-G','edge22-G']
        self.in_edges['H'] = ['edgeI-H', 'edgeE-H','edgeG-H','edge23-H']
        self.in_edges['I'] = ['edge20-I', 'edgeF-I','edgeH-I','edge24-I']
    def getInEdges(self):
        return self.in_edges
