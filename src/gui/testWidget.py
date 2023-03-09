from PyQt5 import QtWidgets, QtTest
from PyQt5.QtCore import QSize, Qt
from algorithms import FordFulkerson, EdmondsKarp, Dinic, PreflowPush
from datetime import datetime
import os.path
from algorithms import Graph

class TestWidget(QtWidgets.QGroupBox):

    def __init__(self, parent):
        super(TestWidget, self).__init__()

        self.parent = parent
        self.graph = None
        self.triples = []

        self.setFixedSize(300, 680)
        self.setTitle("Testumgebung")
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
        self.instancesLabel = QtWidgets.QLabel("Anzahl Instanzen:")
        self.instancesLabel.setFixedHeight(15)
        self.instancesInput = QtWidgets.QLineEdit()
        self.nodeLabel = QtWidgets.QLabel("Knotenzahl:")
        self.nodeLabel.setFixedHeight(15)
        self.nodeInput = QtWidgets.QLineEdit()
        self.capacityLabel = QtWidgets.QLabel("Maximale Kapazität:")
        self.capacityLabel.setFixedHeight(15)
        self.capacityInput = QtWidgets.QLineEdit()
        self.manuallyLabel = QtWidgets.QLabel("... oder manuell Tripelfolge eingeben:")
        self.manuallyLabel.setFixedHeight(15)
        self.manuallyInput = QtWidgets.QLineEdit()
        self.manuallyInput.setPlaceholderText("(a, b, c), (d, e, f), ...")
        self.addButton = QtWidgets.QPushButton(text="Hinzufügen")
        self.addButton.setFixedHeight(50)
        self.addButton.clicked.connect(self.add)
        self.listView = QtWidgets.QListWidget()
        self.startButton = QtWidgets.QPushButton(text="Start")
        self.startButton.setFixedHeight(50)
        self.startButton.clicked.connect(self.start)
        self.startButton.setEnabled(False)
        self.removeButton = QtWidgets.QPushButton(text="Alle entfernen")
        self.removeButton.setFixedHeight(50)
        self.removeButton.clicked.connect(self.removeAll)
        self.removeButton.setEnabled(False)
        # self.progressLabel = QtWidgets.QLabel("Fortschritt:")
        # self.progressLabel.setFixedHeight(15)
        # self.progressValueLabel = QtWidgets.QLabel("0%")
        # self.progressLabel.setFixedHeight(15)
        # self.progress = QtWidgets.QProgressBar()
        # self.progress.setFixedHeight(25)
        # self.progress.setStyleSheet("""
        #     QProgressBar {
        #         text-align: center;
        #     }""")

        self.grid.addWidget(self.instancesLabel, 0, 0, 1, 4)
        self.grid.addWidget(self.instancesInput, 1, 0, 1, 4)
        self.grid.addWidget(self.nodeLabel, 2, 0, 1, 4)
        self.grid.addWidget(self.nodeInput, 3, 0, 1, 4)
        self.grid.addWidget(self.capacityLabel, 4, 0, 1, 4)
        self.grid.addWidget(self.capacityInput, 5, 0, 1, 4)
        self.grid.addWidget(self.manuallyLabel, 6, 0, 1, 4)
        self.grid.addWidget(self.manuallyInput, 7, 0, 1, 4)
        self.grid.addWidget(self.addButton, 8, 0, 1, 4)
        self.grid.addWidget(self.listView, 9, 0, 1, 4)
        self.grid.addWidget(self.startButton, 13, 0, 1, 2)
        self.grid.addWidget(self.removeButton, 13, 2, 1, 2)
        # self.grid.addWidget(self.progressLabel, 12, 0, 1, 3)
        # self.grid.addWidget(self.progressValueLabel, 12, 3, 1, 1)
        # self.grid.addWidget(self.progress, 13, 0, 1, 4)

        self.setLayout(self.grid)



    def add(self):
        instances = self.instancesInput.text()
        nodes = self.nodeInput.text()
        capacity = self.capacityInput.text()
        tripleStrings = self.manuallyInput.text()
        if instances.isdigit() and nodes.isdigit() and capacity.isdigit() and "0" not in [instances, nodes, capacity] and nodes != "1":
            if (int(instances), int(nodes), int(capacity)) not in self.triples:
                self.addItemToList("(" + instances + ", " + nodes + ", " + capacity + ")")
                self.triples.append((int(instances), int(nodes), int(capacity)))
        elif len(tripleStrings) > 6 and tripleStrings[0] == "(" and tripleStrings[-1] == ")":
            tripleStrings = tripleStrings.replace(" ", "")
            tripleStrings = tripleStrings.split("),")
            for i in range(0, len(tripleStrings)):
                tripleStrings[i] = tripleStrings[i].strip("(")
                tripleStrings[i] = tripleStrings[i].strip(")")
                tripleStrings[i] = tripleStrings[i].split(",")
                triple = tripleStrings[i]
                if triple[0].isdigit() and triple[1].isdigit() and triple[2].isdigit() and int(triple[0]) > 0 and int(triple[1]) > 1 and int(triple[2]) > 1 and (int(triple[0]), int(triple[1]), int(triple[2])) not in self.triples:
                    self.triples.append((int(triple[0]), int(triple[1]), int(triple[2])))
                    self.addItemToList("(" + triple[0] + ", " + triple[1] + ", " + triple[2] + ")")
        self.startButton.setEnabled(not self.listView.count() == 0)
        self.removeButton.setEnabled(not self.listView.count() == 0)



    def addItemToList(self, text):
        widget = ListWidget(self)
        widget.setText(text)
        item = QtWidgets.QListWidgetItem(self.listView)
        item.setSizeHint(QSize(0, 40))
        item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
        self.listView.addItem(item)
        self.listView.setItemWidget(item, widget)
        widget.item = item



    def remove(self, row):
        self.listView.takeItem(row)
        del self.triples[row]
        self.startButton.setEnabled(self.listView.count() > 0)
        self.removeButton.setEnabled(self.listView.count() > 0)



    def removeAll(self):
        for row in range(self.listView.count()-1, -1, -1):
            self.remove(row)



    def start(self):
        #(45, 11, 9), (45, 11, 12), (45, 11, 15), (45, 11, 18), (45, 11, 21), (45, 20, 9), (45, 20, 12), (45, 20, 15), (45, 20, 18), (45, 20, 21), (45, 20, 24), (45, 25, 30), (45, 35, 45), (45, 40, 15), (45, 40, 30), (45, 40, 50), (45, 50, 15), (45, 50, 30), (45, 50, 45), (45, 50, 60), (45, 60, 15), (45, 60, 30), (45, 60, 45), (45, 60, 50), (45, 60, 75)
        completed = 0
        self.addButton.setEnabled(False)
        testLog = ["Testeingabe:", str(self.triples), ""]
        totalInstances = 0
        currentInstance = 0
        totalErrors = 0
        totalFlowBreaches = 0
        totalCapacityBreaches = 0
        totalSaturationBreaches = 0

        for instances, _, _ in self.triples:
            totalInstances += instances

        for instanceAmount, nodeAmount, maxCapacity in self.triples:
            testLog += ["Instanzen: " + str(instanceAmount), "Knotenanzahl: " + str(nodeAmount), "Maximale Kapazität: " + str(maxCapacity), ""]
            testLog.append("\n########## Neues Tupel ##########\n")
            for i in range(instanceAmount):
                testLog.append("\n########## Neue Instanz ##########\n")
                currentInstance += 1
                self.graph = Graph(nodeAmount, maxCapacity)

                fordFulkersonResult = FordFulkerson(self.graph).loop()
                flowConditions, capacityConditions, saturationConditions = self.checkConditions()
                if not flowConditions:
                    totalFlowBreaches += 1
                if not capacityConditions:
                    totalCapacityBreaches += 1
                if not saturationConditions:
                    totalSaturationBreaches += 1
                flowConditionsBreach = "Nein" if flowConditions else "Ja"
                capacityConditionsBreach = "Nein" if capacityConditions else "Ja"
                saturationConditionsBreach = "Nein" if saturationConditions else "Ja"
                testLog.append("Ford-Fulkerson Ergebnis: " + str(fordFulkersonResult) + "   Verletzung Flussbedingungen: " + str(flowConditionsBreach) + "   Verletzung Kapazitätsbedingungen: " + str(capacityConditionsBreach) + "   Verletzung Saturierung: " + str(saturationConditionsBreach))
                self.reset()

                edmondsKarpResult = EdmondsKarp(self.graph).loop()
                flowConditions, capacityConditions, saturationConditions = self.checkConditions()
                if not flowConditions:
                    totalFlowBreaches += 1
                if not capacityConditions:
                    totalCapacityBreaches += 1
                if not saturationConditions:
                    totalSaturationBreaches += 1
                flowConditionsBreach = "Nein" if flowConditions else "Ja"
                capacityConditionsBreach = "Nein" if capacityConditions else "Ja"
                saturationConditionsBreach = "Nein" if saturationConditions else "Ja"
                testLog.append("Edmonds-Karp Ergebnis: " + str(edmondsKarpResult) + "   Verletzung Flussbedingungen: " + str(flowConditionsBreach) + "   Verletzung Kapazitätsbedingungen: " + str(capacityConditionsBreach) + "   Verletzung Saturierung: " + str(saturationConditionsBreach))
                self.reset()

                dinicResult = Dinic(self.graph).loop()
                flowConditions, capacityConditions, saturationConditions = self.checkConditions()
                if not flowConditions:
                    totalFlowBreaches += 1
                if not capacityConditions:
                    totalCapacityBreaches += 1
                if not saturationConditions:
                    totalSaturationBreaches += 1
                flowConditionsBreach = "Nein" if flowConditions else "Ja"
                capacityConditionsBreach = "Nein" if capacityConditions else "Ja"
                saturationConditionsBreach = "Nein" if saturationConditions else "Ja"
                testLog.append("Dinic Ergebnis: " + str(dinicResult) + "   Verletzung Flussbedingungen: " + str(flowConditionsBreach) + "   Verletzung Kapazitätsbedingungen: " + str(capacityConditionsBreach) + "   Verletzung Saturierung: " + str(saturationConditionsBreach))
                self.reset()

                preflowPushResult = PreflowPush(self.graph).loop()
                flowConditions, capacityConditions, saturationConditions = self.checkConditions()
                if not flowConditions:
                    totalFlowBreaches += 1
                if not capacityConditions:
                    totalCapacityBreaches += 1
                if not saturationConditions:
                    totalSaturationBreaches += 1
                flowConditionsBreach = "Nein" if flowConditions else "Ja"
                capacityConditionsBreach = "Nein" if capacityConditions else "Ja"
                saturationConditionsBreach = "Nein" if saturationConditions else "Ja"
                testLog.append("Preflow-Push Ergebnis: " + str(preflowPushResult) + "   Verletzung Flussbedingungen: " + str(flowConditionsBreach) + "   Verletzung Kapazitätsbedingungen: " + str(capacityConditionsBreach) + "   Verletzung Saturierung: " + str(saturationConditionsBreach))
                self.reset()

                error = not (fordFulkersonResult == edmondsKarpResult and edmondsKarpResult == dinicResult and dinicResult == preflowPushResult)

                if error:
                    totalErrors += 1

                same = "Ja" if not error else "Nein"
                testLog.append("Anzahl ungleicher Ergebnisse: " + same)
                print(str(round(currentInstance / totalInstances * 100, 2)) + "%")
            # progress = currentInstance / totalInstances * 100
            # self.progress.setValue(progress)
            # self.progressValueLabel.setText(str(self.progress.value()) + "%")

        testLog += ["#################### Testergebnisse ####################", "Instanzen insgesamt: " + str(totalInstances), "Fehler insgesamt: " + str(totalErrors), "Verletzung Flussbedingungen insgesamt: " + str(totalFlowBreaches), "Verletzung Kapazitätsbedingungen insgesamt: " + str(totalCapacityBreaches),  "Verletzung Saturierung: " + str(totalSaturationBreaches)]

        currentDirectory = current_directory = os.path.dirname(__file__)
        parentDirectory = os.path.split(current_directory)[0]
        mainDirectory = os.path.split(parentDirectory)[0]

        now = datetime.now()
        dateString = now.strftime("%d-%m-%Y %H:%M:%S")

        with open(mainDirectory + '/testLogs/testLog_' + dateString + '.txt', 'w') as f:
            for line in testLog:
                f.write(line)
                f.write('\n')

        self.addButton.setEnabled(True)



    def reset(self):
        for i in range(self.graph.nodeAmount):
            for j in range(self.graph.nodeAmount):
                if self.graph.adjMatrix[i][j] is not None and self.graph.adjMatrix[i][j].flow > 0:
                    self.graph.adjMatrix[i][j].flow = 0
            # self.graph.nodes[i] = ""



    def checkConditions(self):

        outflows = [0] * self.graph.nodeAmount
        inflows = [0] * self.graph.nodeAmount
        flowCondition = True
        capacityCondition = True
        saturationCondition = True

        # Für jede Knoten
        # Jeweils eingehende und ausgehende Flows summieren und dann Differenz bilden
        # Differenz ist Überschuss
        # Für alle ausgehenden Kanten überprüfen, ob Überschuss größer als Restkapazität
        # Wenn für eine ja => return false

        for i in range(self.graph.nodeAmount):
            for j in range(self.graph.nodeAmount):

                if self.graph.adjMatrix[i][j] is not None and self.graph.adjMatrix[i][j].capacity > 0:
                    outflows[i] += self.graph.adjMatrix[i][j].flow
                    inflows[j] += self.graph.adjMatrix[i][j].flow

                if self.graph.adjMatrix[i][j] is not None and ((self.graph.adjMatrix[i][j].capacity == 0 and self.graph.adjMatrix[i][j].flow > 0) or (self.graph.adjMatrix[i][j].capacity > 0 and self.graph.adjMatrix[i][j].flow > self.graph.adjMatrix[i][j].capacity)):
                    capacityCondition = False

        del outflows[0]
        del outflows[-1]
        del inflows[0]
        del inflows[-1]

        for i in range(len(outflows)):
            if inflows[i] - outflows[i] != 0:
                flowCondition = False
                break

        return flowCondition, capacityCondition, saturationCondition



class ListWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, item=None):
        super(ListWidget, self).__init__(parent)
        self.parent = parent
        self.item = item
        self.grid = QtWidgets.QGridLayout()
        self.textLabel = QtWidgets.QLabel()
        self.removeButton = QtWidgets.QPushButton(text="Entfernen")
        self.removeButton.clicked.connect(self.remove)
        self.grid.addWidget(self.textLabel, 0, 0, 1, 2)
        self.grid.addWidget(self.removeButton, 0, 3, 1, 1)
        self.setLayout(self.grid)



    def setText (self, text):
        self.textLabel.setText(text)



    def remove(self):
        self.parent.remove(self.parent.listView.indexFromItem(self.item).row())
