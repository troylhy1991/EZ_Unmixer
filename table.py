import re
import operator
import os
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import numpy as np

def main():
    app = QApplication(sys.argv)
    tabledata = [['1','2','3','4','5','6','7','8','9'],
                      ['2','4','5','7','7','23','12','24','10'],
                      ['3','12','31','4','5','6','7','8','9'],
                      ['4','21','32','2','5','6','7','8','9']]
    w = Table(tabledata)
    w.show()
    sys.exit(app.exec_())

class Table(QMainWindow):
    def __init__(self, feature_table):
        QWidget.__init__(self)

        self.object_selected = 0
        self.feature_table = feature_table
        self.tabledata = feature_table

        export_data_action = QAction('&Export Table',self)
        export_data_action.setShortcut('Ctrl+E')
        export_data_action.triggered.connect(self.export_data)
        menubar = self.menuBar()
        OPTMenu = menubar.addMenu('&Operations')
        OPTMenu.addAction(export_data_action)

        # create table
        #self.get_table_data(feature_table)
        self.table = self.createTable()
        self.table.selectRow(self.object_selected)
        # layout
        # layout = QVBoxLayout()
        # layout.addWidget(self.table)
        # self.setLayout(layout)
        self.setCentralWidget(self.table)
        self.setWindowTitle("EZ Unmixer Sample History")


    def export_data(self):
        path = str(QFileDialog.getExistingDirectory(self,"Save Sample History ..."))
        path = path + "\\"
        filename = path + "sample_history.txt"
        feature_table_np = [[float(y) for y in x] for x in self.feature_table]
        np.savetxt(filename, feature_table_np, fmt = '%d \t %d \t %d \t %d \t %d \t %d \t %1.4f \t %1.4f \t %1.4f')


    def createTable(self):
        # create the view
        # tv = QTableView()
        tv = QTableView()

        # set the table model
        header = ['ID', 'X0', 'Y0', 'X1', 'Y1', 'Area', 'AVG_Intensity_master','AVG_Intensity_leak','Ratio']
        tm = MyTableModel(self.tabledata, header, self)
        tv.setModel(tm)

        # set the minimum size
        tv.setMinimumSize(860, 300)

        # hide grid
        tv.setShowGrid(False)

        # set the font
        font = QFont("Courier New", 8)
        tv.setFont(font)

        # hide vertical header
        vh = tv.verticalHeader()
        vh.setVisible(False)

        # set horizontal header properties
        hh = tv.horizontalHeader()
        hh.setStretchLastSection(True)

        # set column width to fit contents
        tv.resizeColumnsToContents()

        # set row height
        nrows = len(self.tabledata)
        for row in xrange(nrows):
            tv.setRowHeight(row, 18)

        # enable sorting
        tv.setSortingEnabled(True)

        tv.setSelectionBehavior(QAbstractItemView.SelectRows)

        # mouse click setting
        #tv.clicked.connect(self.cell_was_clicked)

        return tv



class MyTableModel(QAbstractTableModel):
    def __init__(self, datain, headerdata, parent=None, *args):
        """ datain: a list of lists
            headerdata: a list of strings
        """
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain
        self.headerdata = headerdata

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.arraydata[index.row()][index.column()])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()

    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.arraydata = sorted(self.arraydata, key=operator.itemgetter(Ncol))
        if order == Qt.DescendingOrder:
            self.arraydata.reverse()
        self.emit(SIGNAL("layoutChanged()"))

if __name__ == "__main__":
    main()
