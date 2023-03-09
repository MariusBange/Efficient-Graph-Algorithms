class PreflowPush():

    def __init__(self, g):

        self.g = g
        self.source = 0
        self.sink = g.nodeAmount-1
        self.height = [0] * g.nodeAmount
        self.excess = [0] * g.nodeAmount
        self.visited = [0] * g.nodeAmount
        self.nodes = [i for i in range(g.nodeAmount) if i != self.source and i != self.sink]
        self.height[self.source] = self.g.nodeAmount
        self.excess[self.source] = float("inf")
        self.inactiveAmount = 0
        self.firstStep = True
        self.toVisualize = False



    def push(self, u, v):
        self.toVisualize = True
        isSaturating = False

        flow = min(self.excess[u], self.g.adjMatrix[u][v].capacity - self.g.adjMatrix[u][v].flow) # Fluss ist entweder gesamter Überschuss von Knoten u oder Restkapazität von Kante u-v
        isSaturating = self.excess[u] >= self.g.adjMatrix[u][v].capacity - self.g.adjMatrix[u][v].flow # push ist saturierend, wenn Überschuss größer ist als Kapazität
        self.g.adjMatrix[u][v].flow += flow # Fluss von u nach v erhöhen
        self.g.adjMatrix[v][u].flow -= flow # Fluss von v nach u verringern
        self.excess[u] -= flow # Überschuss von u verringern
        self.excess[v] += flow # Überschuss von v erhöhen

        if self.g.adjMatrix[u][v].capacity > 0:
            self.g.adjMatrix[u][v].color = 'green' if isSaturating else 'blue'
        else:
            self.g.adjMatrix[v][u].color = (200/255.0, 0/255.0, 255/255.0)



    def relabel(self, u):
        # neue nutzbare Kante schaffen
        self.toVisualize = True

        minHeight = float('inf') # Mindesthöhe sehr groß setzen

        for neighbour in range(self.g.nodeAmount):
            if self.g.adjMatrix[u][neighbour] is not None and self.g.adjMatrix[u][neighbour].capacity - self.g.adjMatrix[u][neighbour].flow > 0: # Für alle Kanten von u zu seinen Nachbarn, die noch Restkapazitäten haben
                minHeight = min(minHeight, self.height[neighbour]) # Höhe des aktuell niedrigsten Nachbarn finden
                self.height[u] = minHeight + 1 # Höhe von u eins höher setzen, als die Höhe des aktuell niedrigsten Nachbarn
                self.g.nodeColors[u] = (150/255.0, 225/255.0, 150/255.0)



    def pushRelabel(self, u):

        while self.excess[u] > 0: # So lange push und relabel anwenden, bis Überschuss von Knoten u 0 ist und somit u nicht mehr aktiv

            if self.visited[u] < self.g.nodeAmount:
                v = self.visited[u]

                if self.g.adjMatrix[u][v] is not None and self.g.adjMatrix[u][v].capacity - self.g.adjMatrix[u][v].flow > 0 and self.height[u] > self.height[v]: # Wenn v näher an Zielknoten als u, push
                    self.push(u, v)

                else:
                    self.visited[u] += 1

            else:
                self.relabel(u)
                self.visited[u] = 0



    def step(self):

        self.toVisualize = False

        if self.firstStep: # Im ersten Schritt vom Startknoten aus die Kapazität aller benachbarten Kanten voll ausfüllen

            self.firstStep = False

            for node in range(self.g.nodeAmount):

                if self.g.adjMatrix[self.source][node] is not None: # Für alle Nachbarn des Startknotens
                    self.push(self.source, node) # push von Startknoten auf Nachbarn

            return [], None

        self.resetGraphColors()

        while not self.toVisualize:

            if self.inactiveAmount < len(self.nodes): # Solange es noch aktive Knoten gibt

                u = self.nodes[self.inactiveAmount] # Wähle einen aktiven Knoten
                lastHeight = self.height[u] # Speichern der aktuellen Höhe des gewählten Knotens
                self.pushRelabel(u)

                if self.height[u] > lastHeight: # Wenn sich die Höhe des Knotens durch push/relabel erhöht hat

                    self.nodes.insert(0, self.nodes.pop(self.inactiveAmount)) # Ausgewählten Knoten wieder in Menge der aktiven Knoten einfügen
                    self.inactiveAmount = 0 # Alle Knoten wieder aktiv setzen

                else:
                    self.inactiveAmount += 1 # ansonsten ist Knoten inaktiv und Zahl der inaktiven Knoten hat sich erhöht

                if self.toVisualize:
                    return [], None

            else:

                for i, j in self.g.g.edges:
                    if self.g.adjMatrix[i][j].flow > 0:
                        self.g.adjMatrix[i][j].color = 'blue'

                return None, sum((self.g.adjMatrix[self.source][i].flow if self.g.adjMatrix[self.source][i] is not None else 0) for i in range(self.g.nodeAmount))



    def loop(self):

        for node in range(self.g.nodeAmount):

            if self.g.adjMatrix[self.source][node] is not None:
                self.push(self.source, node)

        self.inactiveAmount = 0

        while self.inactiveAmount < len(self.nodes):

            u = self.nodes[self.inactiveAmount]
            lastHeight = self.height[u]
            self.pushRelabel(u)

            if self.height[u] > lastHeight:

                self.nodes.insert(0, self.nodes.pop(self.inactiveAmount))
                self.inactiveAmount = 0

            else:
                self.inactiveAmount += 1

        return sum((self.g.adjMatrix[self.source][i].flow if self.g.adjMatrix[self.source][i] is not None else 0) for i in range(self.g.nodeAmount))



    def resetGraphColors(self):

        for i, j in self.g.g.edges:
            self.g.adjMatrix[i][j].color = 'black'

        for i in range(len(self.g.nodeColors)):
            if i == 0:
                self.g.nodeColors[i] = (255/255.0, 225/255.0, 150/255.0)
            elif i == len(self.g.nodeColors) - 1:
                self.g.nodeColors[i] = (255/255.0, 150/255.0, 225/255.0)
            else:
                self.g.nodeColors[i] = 'lightgray'
