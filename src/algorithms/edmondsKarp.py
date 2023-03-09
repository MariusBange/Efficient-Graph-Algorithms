class EdmondsKarp():

    def __init__(self, g):

        self.g = g
        self.source = 0
        self.sink = g.nodeAmount - 1
        self.maxFlow = None
        self.lastPath = None


    def bfs(self):

        queue = [self.source]
        paths = {self.source: []}

        if self.source == self.sink:

            return paths[self.source]

        while queue:

            node = queue.pop(0)

            for neighbour in range(self.g.nodeAmount):

                if self.g.adjMatrix[node][neighbour] is not None and self.g.adjMatrix[node][neighbour].capacity - self.g.adjMatrix[node][neighbour].flow > 0 and neighbour not in paths:

                    paths[neighbour] = paths[node] + [(node, neighbour)]

                    if neighbour == self.sink:

                        return paths[neighbour]

                    queue.append(neighbour)
        return



    def step(self):

        path = self.bfs() # Mit Breitensuche Weg von Start- zu Zielknoten suchen

        if path is not None: # Wenn ein Weg gefunden wurde

            flow = min(self.g.adjMatrix[u][v].capacity - self.g.adjMatrix[u][v].flow for u, v in path) # Fluss auf Weg um kleinste Restkapazität auf dem Weg erhöhen (und in andere Richtung entsprechend verringern)

            for u, v in path:
                self.g.adjMatrix[u][v].flow += flow
                self.g.adjMatrix[v][u].flow -= flow

        if self.lastPath is not None:

            for u, v in self.lastPath:
                self.g.adjMatrix[u][v].color = "black"

        if path is not None:

            for u, v in path:
                self.g.adjMatrix[u][v].color = "blue"

        else: # Wenn kein Weg mehr gefunden wurde, gebe aktuellen Fluss zurück

            for u, v in self.g.g.edges:

                if self.g.adjMatrix[u][v].flow > 0:
                    self.g.adjMatrix[u][v].color = "blue"

            self.maxFlow = sum((self.g.adjMatrix[self.source][i].flow if self.g.adjMatrix[self.source][i] is not None else 0) for i in range(self.g.nodeAmount))

        self.lastPath = path

        return path, self.maxFlow



    def loop(self):

        path = self.bfs()

        while path is not None:

            flow = min(self.g.adjMatrix[u][v].capacity - self.g.adjMatrix[u][v].flow for u, v in path)

            for u, v in path:
                self.g.adjMatrix[u][v].flow += flow
                self.g.adjMatrix[v][u].flow -= flow

            path = self.bfs()

        self.maxFlow = sum((self.g.adjMatrix[self.source][i].flow if self.g.adjMatrix[self.source][i] is not None else 0) for i in range(self.g.nodeAmount))

        return self.maxFlow
