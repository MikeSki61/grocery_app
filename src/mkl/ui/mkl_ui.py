from PyQt5 import QtWidgets, QtCore, QtGui


class GroceryApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MKL Grocery List")
        self.setGeometry(100, 100, 600, 100)

    def run(self):
        self.show()
                        
