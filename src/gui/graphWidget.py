import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import sys
sys.path.append("..")
from algorithms import Graph

class GraphWidget(FigureCanvasQTAgg):

    def __init__(self, graph = None, pos = None, nodeAmount = None, capacity = None):

        if graph is not None or (nodeAmount is not None and capacity is not None):

            self.updateGraph(graph, pos, nodeAmount, capacity)
            super(GraphWidget, self).__init__(plt.gcf())
        else:
            super(GraphWidget, self).__init__(plt.figure())

        self.setFixedSize(1400, 1000)



    def drawGraph(self):
        plt.clf()
        plt.figure()
        edgeColors = [self.graph.adjMatrix[i][j].color for i, j in self.graph.g.edges]
        edgeWidths = [0.2+self.graph.adjMatrix[i][j].flow*0.1 for i, j in self.graph.g.edges]
        nodes = {node: "" for node in self.graph.g.nodes()} if self.graph.preflowPush is None else {node: self.graph.preflowPush.height[node] for node in range(len(self.graph.preflowPush.height))}
        nodes = nodes if self.graph.dinic is None else {node: self.graph.dinic.level[node] for node in range(len(self.graph.dinic.level))}
        nx.draw(
            self.graph.g, self.pos,
            edge_color=edgeColors, width=edgeWidths, linewidths=0,
            node_size=40, node_color=self.graph.nodeColors, alpha=1,
            arrows=True, arrowsize=5, arrowstyle='-|>',
            labels=nodes, font_size='3', font_weight='bold', horizontalalignment='center', verticalalignment='center'
        )
        edgeLabels = {(i, j): str(self.graph.adjMatrix[i][j].flow) + "/" + str(self.graph.adjMatrix[i][j].capacity) + "  " + str(self.graph.adjMatrix[j][i].flow) + "/" + str(self.graph.adjMatrix[j][i].capacity) for i, j in self.graph.g.edges if self.graph.adjMatrix[i][j] is not None and self.graph.adjMatrix[i][j].capacity > 0}
        nx.draw_networkx_edge_labels(
            self.graph.g, self.pos,
            edge_labels=edgeLabels, font_color='red', font_size='3', rotate=True,
            #bbox=dict(boxstyle='round', alpha=0.75, ec=(1,1,1), fc=(1,1,1))
        )
        plt.axis('off')



    def updateGraph(self, graph, pos, nodeAmount, capacity):
        self.graph = Graph(nodeAmount, capacity) if graph is None else graph

        # pos = nx.spring_layout(self.graph.g)
        self.pos = nx.planar_layout(self.graph.g) if pos is None else pos
        self.drawGraph()
