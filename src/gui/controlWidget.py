from PyQt5 import QtWidgets, QtCore, QtTest
from . import GraphWidget
import networkx as nx
from algorithms import FordFulkerson, EdmondsKarp, Dinic, PreflowPush

class ControlWidget(QtWidgets.QGroupBox):

    def __init__(self, parent):
        super(ControlWidget, self).__init__()

        self.parent = parent
        self.isPlaying = False
        self.graphWidget = None
        self.lastPath = None

        self.setFixedSize(300, 300)
        self.setTitle("Einstellungen")
        self.setStyleSheet("""
            QGroupBox {
                border: 2px solid lightgray;
                border-radius: 5px;
                padding: 5px
            }

            QGroupBox::title {
                subcontrol-origin: top;
                subcontrol-position: top center; /* position at the top center */
                padding: 1 5px;
                background-color: lightgray;
            }""")

        self.grid = QtWidgets.QGridLayout()
        self.ticksLabel = QtWidgets.QLabel("Ticks:")
        self.ticksLabel.setFixedSize(75, 15)
        self.nodeLabel = QtWidgets.QLabel("Knotenzahl:")
        self.nodeLabel.setFixedSize(150, 15)
        self.capacityLabel = QtWidgets.QLabel("Kapazität:")
        self.capacityLabel.setFixedSize(150, 15)
        self.algorithmLabel = QtWidgets.QLabel("Algorithmus:")
        self.algorithmLabel.setFixedSize(150, 15)
        self.nodeInput = QtWidgets.QLineEdit()
        self.nodeInput.textChanged.connect(self.nodeChange)
        self.capacityInput = QtWidgets.QLineEdit()
        self.capacityInput.textChanged.connect(self.capacityChange)
        self.algorithmInput = QtWidgets.QComboBox()
        self.algorithmInput.addItems(["Ford-Fulkerson", "Edmonds-Karp", "Dinic", "Preflow-Push"])
        self.algorithmInput.currentIndexChanged.connect(self.reset)
        self.createButton = QtWidgets.QPushButton(text="Graphen erstellen")
        self.createButton.setEnabled(False)
        self.createButton.clicked.connect(self.createGraph)
        self.deleteButton = QtWidgets.QPushButton(text="Graphen löschen")
        self.deleteButton.setEnabled(False)
        self.deleteButton.clicked.connect(self.deleteGraph)
        self.playButton = QtWidgets.QPushButton(icon=self.style().standardIcon(getattr(QtWidgets.QStyle, "SP_MediaPlay")))
        self.playButton.setFixedSize(55, 50)
        self.playButton.setEnabled(False)
        self.playButton.clicked.connect(self.play)
        self.resetButton = QtWidgets.QPushButton(text="Zurücksetzen")
        self.resetButton.setEnabled(False)
        self.resetButton.clicked.connect(self.reset)
        self.forwardButton = QtWidgets.QPushButton(icon=self.style().standardIcon(getattr(QtWidgets.QStyle, "SP_MediaSkipForward")))
        self.forwardButton.setFixedSize(55, 50)
        self.forwardButton.setEnabled(False)
        self.forwardButton.clicked.connect(self.forward)
        self.speedSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.speedSlider.setMinimum(25)
        self.speedSlider.setMaximum(500)
        self.speedSlider.setValue(25)
        self.speedSlider.setFixedSize(120, 30)
        self.speedSlider.valueChanged.connect(self.sliderChange)
        self.speedLabel = QtWidgets.QLabel(f"{self.speedSlider.value()/100}s")
        self.speedLabel.setFixedSize(75, 15)
        self.messageBox = QtWidgets.QMessageBox()

        self.grid.addWidget(self.nodeLabel, 0, 0, 1, 2)
        self.grid.addWidget(self.capacityLabel, 0, 2, 1, 2)
        self.grid.addWidget(self.nodeInput, 1, 0, 1, 2)
        self.grid.addWidget(self.capacityInput, 1, 2, 1, 2)
        self.grid.addWidget(self.createButton, 2, 0, 1, 4)
        self.grid.addWidget(self.deleteButton, 3, 0, 1, 4)
        self.grid.addWidget(self.algorithmLabel, 4, 0, 1, 4)
        self.grid.addWidget(self.algorithmInput, 5, 0, 1, 4)
        self.grid.addWidget(self.playButton, 6, 0, 1, 1)
        self.grid.addWidget(self.forwardButton, 6, 1, 1, 1)
        self.grid.addWidget(self.resetButton, 6, 2, 1, 2)
        self.grid.addWidget(self.ticksLabel, 7, 0, 1, 1)
        self.grid.addWidget(self.speedLabel, 7, 1, 1, 1)
        self.grid.addWidget(self.speedSlider, 7, 2, 1, 2)

        self.setLayout(self.grid)



    def nodeChange(self):
        nodeValue = self.nodeInput.text()
        capacityValue = self.capacityInput.text()
        self.createButton.setEnabled(nodeValue.isdigit() and capacityValue.isdigit() and "0" not in [nodeValue[0], capacityValue[0]] and nodeValue != "1")



    def capacityChange(self):
        nodeValue = self.nodeInput.text()
        capacityValue = self.capacityInput.text()
        self.createButton.setEnabled(nodeValue.isdigit() and capacityValue.isdigit() and "0" not in [nodeValue[0], capacityValue[0]] and nodeValue != "1")



    def createGraph(self):
        nodeAmount = int(self.nodeInput.text())
        capacity = int(self.capacityInput.text())

        self.updateGraphWidget(GraphWidget(None, None, nodeAmount, capacity))
        self.setElements(True, [self.deleteButton, self.playButton, self.forwardButton, self.resetButton])
        self.lastPath = None



    def deleteGraph(self):
        self.updateGraphWidget(GraphWidget())
        self.setElements(False, [self.deleteButton, self.playButton, self.forwardButton, self.resetButton])
        self.setElements(False, [self.resetButton])
        self.lastPath = None



    def play(self):
        self.isPlaying = not self.isPlaying
        if self.isPlaying:
            self.setElements(False, [self.createButton, self.deleteButton, self.algorithmInput, self.forwardButton, self.resetButton])
            self.playButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, "SP_MediaPause")))
            while self.isPlaying:
                waitTime = self.speedSlider.value()*10
                self.setElements(False, [self.resetButton, self.forwardButton])
                self.forward()
                self.setElements(False, [self.resetButton])
                if self.lastPath is None:
                    self.playButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, "SP_MediaPlay")))
                    self.isPlaying = False
                    self.setElements(True, [self.createButton, self.deleteButton, self.algorithmInput, self.resetButton])
                    break
                QtTest.QTest.qWait(waitTime)
        else:
            self.setElements(True, [self.createButton, self.deleteButton, self.algorithmInput, self.forwardButton, self.resetButton])
            self.playButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, "SP_MediaPlay")))



    def forward(self):
        flow = None
        if self.algorithmInput.currentText() == "Ford-Fulkerson":
            if self.graphWidget.graph.fordFulkerson is None:
                self.graphWidget.graph.fordFulkerson = FordFulkerson(self.graphWidget.graph)
            self.lastPath, flow = self.graphWidget.graph.fordFulkerson.step()
        elif self.algorithmInput.currentText() == "Edmonds-Karp":
            if self.graphWidget.graph.edmondsKarp is None:
                self.graphWidget.graph.edmondsKarp = EdmondsKarp(self.graphWidget.graph)
            self.lastPath, flow = self.graphWidget.graph.edmondsKarp.step()
        elif self.algorithmInput.currentText() == "Dinic":
            if self.graphWidget.graph.dinic is None:
                self.graphWidget.graph.dinic = Dinic(self.graphWidget.graph)
            self.lastPath, flow = self.graphWidget.graph.dinic.step()
        elif self.algorithmInput.currentText() == "Preflow-Push":
            if self.graphWidget.graph.preflowPush is None:
                self.graphWidget.graph.preflowPush = PreflowPush(self.graphWidget.graph)
            self.lastPath, flow = self.graphWidget.graph.preflowPush.step()
        self.setElements(self.lastPath is not None, [self.forwardButton, self.playButton])
        self.updateGraphWidget(GraphWidget(self.graphWidget.graph, self.graphWidget.pos))
        self.resetButton.setEnabled(True)
        if flow is not None:
            self.messageBox.setText(self.algorithmInput.currentText() + " Ergebnis\nMaxFlow: " + str(flow))
            self.messageBox.exec_()



    def reset(self):
        if self.graphWidget is not None:
            for i, j in self.graphWidget.graph.g.edges:
                self.graphWidget.graph.adjMatrix[i][j].flow = 0
                self.graphWidget.graph.adjMatrix[i][j].color = 'black'
            for i in range(len(self.graphWidget.graph.nodeColors)):
                if i == 0:
                    self.graphWidget.graph.nodeColors[i] = (255/255.0, 225/255.0, 150/255.0)
                elif i == len(self.graphWidget.graph.nodeColors) - 1:
                    self.graphWidget.graph.nodeColors[i] = (255/255.0, 150/255.0, 225/255.0)
                else:
                    self.graphWidget.graph.nodeColors[i] = 'lightgray'
            self.graphWidget.graph.fordFulkerson = None
            self.graphWidget.graph.edmondsKarp = None
            self.graphWidget.graph.dinic = None
            self.graphWidget.graph.preflowPush = None
            self.updateGraphWidget(GraphWidget(self.graphWidget.graph, self.graphWidget.pos))
            self.setElements(True, [self.deleteButton, self.playButton, self.algorithmInput, self.forwardButton])
            self.setElements(False, [self.resetButton])
            self.lastPath = None
            self.isPlaying = False
            flow = None



    def sliderChange(self):
        value = round(self.speedSlider.value()/25)*25
        self.speedSlider.setValue(value)
        self.speedLabel.setText(f"{self.speedSlider.value()/100}s")



    def updateGraphWidget(self, widget):
        self.graphWidget = widget
        self.parent.hLayout.replaceWidget(self.parent.graph, self.graphWidget)
        self.parent.graph = self.graphWidget



    def setElements(self, state, elements):
        for element in elements:
            element.setEnabled(state)
