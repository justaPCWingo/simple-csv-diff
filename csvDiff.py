from __future__ import absolute_import, division, print_function, unicode_literals

import csv
import sys
import os
from argparse import ArgumentParser
from PyQt5 import QtWidgets
try:
    from MainWindow import MainWindow
except ImportError:
    from .MainWindow import MainWindow

class CsvRec(object):
    def __init__(self,path):
        
        self.modTime = os.stat(path).st_mtime
        self.path = path
        
        self._Reload()
        
    
    def _Reload(self):
        with open(self.path,'r') as inFile:
            rdr = csv.DictReader(inFile)
            self.data=[r for r in rdr]
            self.keys=rdr.fieldnames
    
    def NeedsRefresh(self):
        return os.stat(self.path).st_mtime > self.modTime
        
    def RefreshIfNeeded(self):
        
        if self.NeedsRefresh():
            self._Reload()
            return True
        return False
            
def runcCsvDiff():

    prsr = ArgumentParser(description="Interactive tool for comparing csv columns")
    prsr.add_argument("csv1", type=str, help="First File to compare")
    prsr.add_argument("csv2", type=str, help="Second File to compare")

    args = prsr.parse_args()

    f1 = CsvRec(args.csv1)
    f2 = CsvRec(args.csv2)
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow(f1, f2)

    mainWindow.show()
    sys.exit(app.exec_())

if __name__=='__main__':
    runcCsvDiff()
