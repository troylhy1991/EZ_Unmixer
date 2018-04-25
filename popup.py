from PyQt4.QtGui import *
from PyQt4.QtCore import *


class MyPopup(QWidget):
    def __init__(self, parent=None):
        super(MyPopup, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.label = QLabel("Unmix Ratio :")
        self.textbox = QLineEdit(self)
        self.textbox.setText("0.7")
        self.button = QPushButton('Set', self)
        self.button.clicked.connect(self.setvalue)

        HLayoutBox = QHBoxLayout()
        HLayoutBox.addWidget(self.label)
        HLayoutBox.addWidget(self.textbox)

        VLayoutBox = QVBoxLayout()
        VLayoutBox.addLayout(HLayoutBox)

        VLayoutBox.addWidget(self.button)
        self.setLayout(VLayoutBox)
        self.resize(300,150)

        self.setWindowTitle('Set Ratio')
        self.show()

    def setvalue(self):
        self.ratio= float(self.textbox.text())
        self.emit(SIGNAL("SET_RATIO"),self.ratio)
