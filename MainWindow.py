from __future__ import absolute_import, division, print_function, unicode_literals

import os
from Ui_MainWindow import Ui_MainWindow

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant

from PyQt5.QtWidgets import QMainWindow

class TableModel(QAbstractTableModel):

    def __init__(self,c1,c2,key,parent=None):
        QAbstractTableModel.__init__(self,parent)

        self._c1=c1
        self._c2=c2

        self.selectedKey = key
        self.headers=[os.path.basename(c1.path),os.path.basename(c2.path),"Diff"]
        
        
    def rowCount(self, parent=QModelIndex()):
        return max(len(self._c1.data),len(self._c2.data))

    def columnCount(self, parent=QModelIndex()):
        return 3

    def data(self, index, role=Qt.DisplayRole):
        
        r = index.row()
        c = index.column()
        k = self.selectedKey
        if role == Qt.DisplayRole:
            if c == 0 and len(self._c1.data)>r:
                return self._c1.data[r][k]
            elif c == 1 and len(self._c2.data)>r:
                return self._c2.data[r][k]
            elif c == 2:
                try:
                    return QVariant(abs(float(self._c1.data[r][k])-float(self._c2.data[r][k])))
                except:
                    return QVariant("N/A")
        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):

        if role == Qt.DisplayRole and orientation==Qt.Horizontal:
            return QVariant(self.headers[section])
        return QVariant()

    def sumDiffs(self):
        if len(self._c1.data)!=len(self._c2.data):
            return None
        tot=0
        k = self.selectedKey
        for i in range(len(self._c1.data)):
            tot+=abs(float(self._c1.data[i][k]) - float(self._c2.data[i][k]))
        
        return tot
    
    def refreshIfNeeded(self):
        return self._c1.RefreshIfNeeded() or self._c2.RefreshIfNeeded()

class MainWindow(QMainWindow):
    def __init__(self,c1,c2,parent=None):
        QMainWindow.__init__(self,parent)

        ui=Ui_MainWindow()
        ui.setupUi(self)

        colKeys = list(set(c1.keys).intersection(c2.keys))

        self._mdl=TableModel(c1,c2,colKeys[0],self)
        ui.tableView.setModel(self._mdl)
        self._ui=ui

        ui.columnCombo.addItems(colKeys)
        ui.columnCombo.currentTextChanged.connect(self.updateCols)
        ui.columnCombo.setCurrentText(colKeys[0])
        self.updateCols()

    def updateCols(self):
        self._mdl.selectedKey = self._ui.columnCombo.currentText()
        tot = self._mdl.sumDiffs()

        self._ui.diffSumField.setText(str(tot) if tot is not None else "--")
        self._ui.tableView.reset()

    def setFocus(self):

        if self._mdl.refreshIfNeeded():
            self._ui.tableView.reset()
        QMainWindow.setFocus(self)
