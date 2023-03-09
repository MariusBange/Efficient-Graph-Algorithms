from random import randint
import itertools as it
import networkx as nx


class Graph():

    def __init__(self, nodeAmount: int, capacity: int):


        self.adjMatrix = [[None for i in range(nodeAmount)] for j in range(nodeAmount)]
        self.maxCapacity = capacity
        self.nodeAmount = nodeAmount
        self.nodes, self.nodeColors = [], []
        self.createNodes()
        self.g = nx.DiGraph()
        self.g.add_nodes_from(self.nodes)
        self.createEdges()

        self.fordFulkerson = None
        self.edmondsKarp = None
        self.dinic = None
        self.preflowPush = None



    def createNodes(self):

        for i in range(0, self.nodeAmount):
            self.nodes.append(i)
            if i == 0:
                self.nodeColors.append((255/255.0, 225/255.0, 150/255.0))#(160/255.0, 150/255.0, 255/255.0)
            elif i == self.nodeAmount - 1:
                self.nodeColors.append((255/255.0, 150/255.0, 225/255.0))
            else:
                self.nodeColors.append('lightgray')



    def createEdges(self):

        possibleEdges = [pair for pair in it.permutations(self.nodes, 2)]

        i = 0
        while i < len(possibleEdges):
            if possibleEdges[i][1] == 0 or possibleEdges[i][0] == self.nodeAmount-1:
                del possibleEdges[i]
                i -= 1
            i += 1

        while len(possibleEdges) > 0:
            edge = possibleEdges[randint(0, len(possibleEdges)-1)]
            if self.adjMatrix[edge[0]][edge[1]] is None:
                self.g.add_edge(edge[0], edge[1])
                if not nx.check_planarity(self.g)[0]:
                    self.g.remove_edge(edge[0], edge[1])
                else:
                    capacity = randint(1, self.maxCapacity)# if (edge[0] != 0 and edge[1] != self.nodeAmount-1) else 10000
                    self.adjMatrix[edge[0]][edge[1]] = Edge(edge[0], edge[1], capacity)
                    self.adjMatrix[edge[1]][edge[0]] = Edge(edge[1], edge[0], 0, 0, None)
            possibleEdges.remove(edge)

        # reorder edges in respect to adjMatrix order
        self.g.remove_edges_from(list(self.g.edges()))
        for j in range(self.nodeAmount):
            for k in range(self.nodeAmount):
                if self.adjMatrix[j][k] is not None and self.adjMatrix[j][k].capacity > 0:
                    self.g.add_edge(j, k)



class Edge():

    def __init__(self, start: str, end: str, capacity: int, flow: int = 0, color: str = 'black'):
        self.start = start
        self.end = end
        self.flow = flow
        self.capacity = capacity
        self.color = color
        assert(start != end)
        assert(flow <= capacity)
