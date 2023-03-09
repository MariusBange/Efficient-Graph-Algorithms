import networkx as nx
from copy import deepcopy as dc

class Dinic():

    def __init__(self, g):

        self.g = g
        self.source = 0
        self.sink = g.nodeAmount - 1
        self.maxFlow = None
        self.flow = 0
        self.level = g.nodeAmount * [0]
        self.level[self.source] = 1
        self.visited = [False] * self.g.nodeAmount
        self.path = []
        self.paths = []



    def bfs(self):
        # Mit Breitensuche die Tiefe bzw. "Schicht" von jedem Knoten bestimmen
        # Wenn Zielknoten durch Breitensuche nicht mehr erreicht werden kann (und somit Tiefe 0 hat), ist Dinic fertig

        queue = [self.source]

        self.level = self.g.nodeAmount * [0]
        self.level[self.source] = 1

        while queue:

            node = queue.pop(0)

            for neighbour in range(self.g.nodeAmount):

                if self.g.adjMatrix[node][neighbour] is not None and self.g.adjMatrix[node][neighbour].flow < self.g.adjMatrix[node][neighbour].capacity and (self.level[neighbour] == 0 or neighbour == self.sink):

                    self.level[neighbour] = self.level[node] + 1

                    if neighbour != self.sink:
                        queue.append(neighbour)

        return self.level[self.sink] > 0



    def dfs(self, source, capacity):
        # Mit Tiefensuche

        pathCapacity = capacity # Die Kapazität des aktuellen Weges entspricht der geringsten Restkapazität einer Kante auf dem Weg

        self.visited[source] = True
        self.path.append(source)

        if source == self.sink:

            for i in range(len(self.path)-1):
                self.g.adjMatrix[self.path[i]][self.path[i+1]].color = 'black'
            # Teilmenge von Schichtgraph

            return capacity # Wenn Zielknoten erreicht wurde, kann Weg mit Fluss in Höhe des Wertes der geringsten Kapazität "befüllt" werden

        for neighbour in range(self.g.nodeAmount): # Ansonsten geht die Suche nach dem Zielknoten weiter, indem alle Nachbarn des aktuellen Knoten betrachtet werden
            # print(source, neighbour, self.g.adjMatrix[source][neighbour] is not None and self.level[neighbour] > self.level[source] and self.g.adjMatrix[source][neighbour].flow < self.g.adjMatrix[source][neighbour].capacity)

            # if self.g.adjMatrix[source][neighbour] is not None and self.g.adjMatrix[source][neighbour].capacity > 0:
            #     self.g.adjMatrix[source][neighbour].color = 'green'
            # Alle Kanten

            if self.g.adjMatrix[source][neighbour] is not None and self.level[neighbour] > self.level[source] and self.g.adjMatrix[source][neighbour].flow < self.g.adjMatrix[source][neighbour].capacity:

                flow = self.dfs(neighbour, min(pathCapacity, self.g.adjMatrix[source][neighbour].capacity - self.g.adjMatrix[source][neighbour].flow)) # Flow aller Kanten auf dem Weg zum Zielknoten um geringste Kapazität auf dem Weg erhöhen - auf Weg zurück verringern

                # self.g.adjMatrix[source][neighbour].color = 'red' # Ganzer Schichtgraph aber auch andere Kanten
                self.g.adjMatrix[source][neighbour].flow += flow
                self.g.adjMatrix[neighbour][source].flow -= flow

                pathCapacity -= flow

        # if self.g.adjMatrix[source][neighbour] is not None and self.g.adjMatrix[source][neighbour].capacity > 0:
        #         self.g.adjMatrix[source][neighbour].color = 'yellow'
        # Alle Kanten an Zielknoten

        self.path.pop()
        self.visited[source] = False

        return capacity - pathCapacity



    def step(self):

        nextStep = self.bfs()
        path = 0

        if nextStep:

            for i, j in self.g.g.edges:
                self.g.adjMatrix[i][j].color = (230/255.0, 230/255.0, 230/255.0)

            self.visited = [False] * self.g.nodeAmount
            self.path = []
            # self.paths = []
            # self.getLevelGraph(self.source, self.sink)
            # for x in self.paths:
            #     for i in range(len(x)-1):
            #         self.g.adjMatrix[x[i]][x[i+1]].color = 'black'

            self.flow += self.dfs(self.source, 100000)

            # self.visited = [False] * self.g.nodeAmount
            # self.path = []
            # self.paths = []
            # self.getBlockingFlow(self.source, self.sink)
            # if self.paths:
            #     for i in range(len(self.paths[0])-2):
            #         self.g.adjMatrix[self.paths[0][i]][self.paths[0][i+1]].color = 'green'

        else:
            self.maxFlow = self.flow
            path = None

        return path, self.maxFlow



    def loop(self):

        while self.bfs():

            self.flow += self.dfs(self.source, 100000)

        self.maxFlow = self.flow

        return self.maxFlow



    def getLevelGraph(self, u, v):

        self.visited[u] = True
        self.path.append(u)

        if u == v:
            for i in range(len(self.path)-1):
                self.g.adjMatrix[self.path[i]][self.path[i+1]].color = 'black'
            # self.paths.append(dc(self.path))

        else:
            for neighbour in range(self.g.nodeAmount):
                if self.g.adjMatrix[u][neighbour] is not None and not self.visited[neighbour] and self.g.adjMatrix[u][neighbour].capacity > 0 and self.level[neighbour] > self.level[u]:
                    self.getLevelGraph(neighbour, v)

        self.path.pop()
        self.visited[u] = False



    def getBlockingFlow(self, u, v):
        self.visited[u] = True
        self.path.append(u)

        if u == v:
            self.paths.append(dc(self.path))

        else:
            for neighbour in range(self.g.nodeAmount):
                if self.g.adjMatrix[u][neighbour] is not None and not self.visited[neighbour] and self.g.adjMatrix[u][neighbour].capacity > 0 and self.level[neighbour] > self.level[u] and self.g.adjMatrix[u][neighbour].capacity - self.g.adjMatrix[u][neighbour].flow > 0:
                    self.getLevelGraph(neighbour, v)

        self.path.pop()
        self.visited[u] = False
