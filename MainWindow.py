from __future__ import absolute_import, division, print_function, unicode_literals

import os
try:
    from Ui_MainWindow import Ui_MainWindow
except ImportError:
    from .Ui_MainWindow import Ui_MainWindow

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant,QEvent

from PyQt5.QtWidgets import QMainWindow

class TableModel(QAbstractTableModel):

    def __init__(self,c1,c2,key,parent=None):
        QAbstractTableModel.__init__(self,parent)

        self._c1=c1
        self._c2=c2

        self.selectedKey = key
        self.refKey = key
        self.headers=[key,
                      (os.path.basename(c1.path),c1),
                      (os.path.basename(c2.path),c2),
                      "Diff"]
        
        
    def rowCount(self, parent=QModelIndex()):
        return max(len(self._c1.data),len(self._c2.data))

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        
        r = index.row()
        c = index.column()
        k = self.selectedKey
        k2 = self.refKey
        if role == Qt.DisplayRole:
            if c == 0 and len(self._c1.data)>r:
                try:
                    return str(self._c1.data[r][k2])+'|'+str(self._c2.data[r][k2])
                except:
                    return '--'
            if c == 1 and len(self._c1.data)>r:
                return self._c1.data[r][k]
            elif c == 2 and len(self._c2.data)>r:
                return self._c2.data[r][k]
            elif c == 3:
                try:
                    return QVariant(abs(float(self._c1.data[r][k])-float(self._c2.data[r][k])))
                except:
                    try:
                        return QVariant('' if str(self._c1.data[r][k])==str(self._c2.data[r][k]) else '!!')
                    except:
                        pass
        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        self.headers[0]=self.refKey
        if role == Qt.DisplayRole:
            if orientation==Qt.Horizontal:
                ret=self.headers[section]
                if type(ret)==tuple:
                    ret= ret[0]+" ({})".format(len(ret[1].data))
                return QVariant(ret)
            else:
                return QVariant(section+1)
        return QVariant()

    def sumDiffs(self):
        if len(self._c1.data)!=len(self._c2.data):
            return None
        tot=0
        k = self.selectedKey
        for i in range(len(self._c1.data)):
            try:
              tot+=abs(float(self._c1.data[i][k]) - float(self._c2.data[i][k]))
            except ValueError:
              tot=float("nan")
              break
        
        return tot
    
    def refreshIfNeeded(self):
        r1=self._c1.RefreshIfNeeded()
        r2=self._c2.RefreshIfNeeded()
        return r1 or r2

class MainWindow(QMainWindow):
    def __init__(self,c1,c2,parent=None):
        QMainWindow.__init__(self,parent)

        ui=Ui_MainWindow()
        ui.setupUi(self)

        colKeys = sorted(list(set(c1.keys).intersection(c2.keys)))

        self._mdl=TableModel(c1,c2,colKeys[0],self)
        ui.tableView.setModel(self._mdl)
        self._ui=ui

        ui.columnCombo.addItems(colKeys)
        ui.columnCombo.currentTextChanged.connect(self.updateCols)
        ui.columnCombo.setCurrentText(colKeys[0])
        ui.refCombo.addItems(colKeys)
        ui.refCombo.currentTextChanged.connect(self.updateCols)
        ui.refCombo.addItems(colKeys)
        self.updateCols()


    def updateCols(self):
        self._mdl.selectedKey = self._ui.columnCombo.currentText()
        self._mdl.refKey = self._ui.refCombo.currentText()
        tot = self._mdl.sumDiffs()

        self._ui.diffSumField.setText(str(tot) if tot is not None else "--")
        self._ui.tableView.reset()

    def changeEvent(self,event):
        if hasattr(self,'_ui'):
            self._ui.statusbar.showMessage("Reloading files...")
            if event.type() == QEvent.ActivationChange and self._mdl.refreshIfNeeded():
                print("Reloading")
                tot = self._mdl.sumDiffs()

                self._ui.diffSumField.setText(str(tot) if tot is not None else "--")
                self._ui.tableView.reset()
                self._mdl.headerDataChanged.emit(Qt.Horizontal,1,2)
            self._ui.statusbar.clearMessage()

