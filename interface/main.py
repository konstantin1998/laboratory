#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout
from interface.IQA.generated_gui import Ui_MainWindow
from interface.IQA.quality_estimator.estimator import estimate_quality
"""
print('before')
q = estimate_quality("IQA/St112L_4_V_32_S_649488.6091.bmp")
print(q)
print('after')
"""
class Example(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(Example, self).__init__()
        self.setupUi(self)

        plus_icon = QtGui.QIcon()
        plus_icon.addPixmap(QtGui.QPixmap("IQA/stuff/gui_img/plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_6.setIcon(plus_icon)
        minus_icon = QtGui.QIcon()
        minus_icon.addPixmap(QtGui.QPixmap("IQA/stuff/gui_img/minus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5.setIcon(minus_icon)
        select_area_icon = QtGui.QIcon()
        select_area_icon.addPixmap(QtGui.QPixmap("IQA/stuff/gui_img/select-area.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(select_area_icon)
        delete_icon = QtGui.QIcon()
        delete_icon.addPixmap(QtGui.QPixmap("IQA/stuff/gui_img/del.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_4.setIcon(delete_icon)

        self.curr_img = QtWidgets.QLabel(self.centralwidget)
        self.curr_img.setPixmap(QtGui.QPixmap("IQA/St112L_4_V_54_S_619501.0536.bmp"))
        self.curr_img.setScaledContents(True)
        self.curr_img.setObjectName("label")
        self.gridLayout.addWidget(self.curr_img, 1, 0, 1, 3)

        self.similar_img = QtWidgets.QLabel(self.centralwidget)
        self.similar_img.setPixmap(QtGui.QPixmap("IQA/St112L_4_V_32_S_649488.6091.bmp"))
        self.similar_img.setScaledContents(True)
        self.similar_img.setObjectName("label")
        self.gridLayout.addWidget(self.similar_img, 2, 0, 1, 3)

        q = estimate_quality("IQA/St112L_4_V_32_S_649488.6091.bmp")
        lbl1 = QtWidgets.QLabel('Метрика: ' + str(q))

        self.gridLayout.addWidget(lbl1, 2, 4)
        self.show()

    def get_metrix_label(self, path_to_img):
        hbox = QHBoxLayout()
        lbl1 = QtWidgets.QLabel('Метрика', self.centralwidget)
        value = 1#estimate_quality(path_to_img) / 1000
        lbl2 = QtWidgets.QLabel(str(value), self.centralwidget)
        hbox.addWidget(lbl2)
        hbox.addWidget(lbl1)
        return hbox
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())