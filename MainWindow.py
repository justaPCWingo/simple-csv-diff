from __future__ import absolute_import, division, print_function, unicode_literals

from Ui_MainWindow import Ui_MainWindow

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant

from PyQt5.QtWidgets import QMainWindow

class TableModel(QAbstractTableModel):

    def __init__(self,c1,c2,key,parent=None)
