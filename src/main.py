from PyQt5 import QtWidgets, uic
from gui import GraphWidget, ControlWidget, TestWidget
import networkx as nx


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()

        self.mainWidget = QtWidgets.QWidget()
        self.graph = GraphWidget()
        self.controls = ControlWidget(self)
        self.tests = TestWidget(self)
        self.sideBar = QtWidgets.QWidget()
        self.vLayout = QtWidgets.QVBoxLayout()
        self.vLayout.addWidget(self.controls)
        self.vLayout.addWidget(self.tests)
        self.sideBar.setLayout(self.vLayout)
        self.hLayout = QtWidgets.QHBoxLayout()
        self.hLayout.addWidget(self.graph)
        self.hLayout.addWidget(self.sideBar)
        self.mainWidget.setLayout(self.hLayout)
        self.setCentralWidget(self.mainWidget)
        self.show() # Show the GUI


if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_() # Start the application
