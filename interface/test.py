import sys
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QMessageBox)
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton
from PyQt5 import QtGui

class MyMessageBox(QMessageBox):
    def __init__(self):
        QMessageBox.__init__(self)
        self.setSizeGripEnabled(True)

    def event(self, e):
        result = QMessageBox.event(self, e)

        self.setMinimumHeight(0)
        self.setMaximumHeight(16777215)
        self.setMinimumWidth(0)
        self.setMaximumWidth(16777215)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

        textEdit = self.findChild(QtGui.QTextEdit)
        if textEdit != None :
            textEdit.setMinimumHeight(0)
            textEdit.setMaximumHeight(16777215)
            textEdit.setMinimumWidth(0)
            textEdit.setMaximumWidth(16777215)
            textEdit.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

        return result

if __name__ == '__main__':
    mb = MyMessageBox()
    mb.setText("Results written to '%s'" % 'some_file_name')
    mb.setDetailedText('some text')
    mb.exec_()