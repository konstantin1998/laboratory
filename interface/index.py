import sys
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication, QPushButton
from PyQt5.QtGui import QIcon


class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        window_width = 550
        window_heigth = 250
        window_x, window_y = 300, 300

        #textEdit = QTextEdit()
        #self.setCentralWidget(textEdit)
        exitAction = QAction( 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        self.statusBar()

        menubar = self.menuBar()
        change_data_set_but = menubar.addMenu('сменить набор данных')
        change_data_set_but.addAction(exitAction)
        change_mode_but = menubar.addMenu('Сменить режим разметки')
        upload_but = menubar.addMenu('Выгрузить разметку')
        instruction_but = menubar.addMenu('Инструкция')

        mark_btn = QPushButton('Отметить изображение как лучшее', self)
        mark_btn.setToolTip('This is a <b>QPushButton</b> widget')
        mark_btn.resize(200, 20)
        mark_btn.move(10, 220)

        switch_btn = QPushButton('Следующая пара изображений', self)
        switch_btn.setToolTip('This is a <b>QPushButton</b> widget')
        switch_btn.resize(200, 20)
        switch_btn.move(220, 220)

        self.setGeometry(window_x, window_y, window_width, window_heigth)
        self.setWindowTitle('Main window')
        self.show()

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        # MainWindow.setMaximumSize(QtCore.QSize(900, 600))
        MainWindow.setFixedSize(QtCore.QSize(900, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.dataset_load_pb = QtWidgets.QProgressBar(self.centralwidget)
        self.dataset_load_pb.setProperty("value", 24)
        self.dataset_load_pb.setObjectName("dataset_load_pb")
        self.gridLayout.addWidget(self.dataset_load_pb, 5, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("stuff/gui_img/plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_6.setIcon(icon)
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout.addWidget(self.pushButton_6)
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("stuff/gui_img/minus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5.setIcon(icon1)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout.addWidget(self.pushButton_5)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("stuff/gui_img/select-area.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon2)
        self.pushButton_3.setFlat(False)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("stuff/gui_img/del.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_4.setIcon(icon3)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 2, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setCheckable(False)
        self.pushButton_2.setDefault(False)
        self.pushButton_2.setFlat(False)
        self.pushButton_2.setObjectName("pushButton_2")#следующая пара изображений
        self.gridLayout.addWidget(self.pushButton_2, 4, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setText("")
        """
        self.label.setPixmap(QtGui.QPixmap("default2.bmp"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 3)
        """
        self.curr_img = QtWidgets.QLabel(self.centralwidget)
        self.curr_img.setPixmap(QtGui.QPixmap("default2.bmp"))
        self.curr_img.setScaledContents(True)
        self.curr_img.setObjectName("label")
        self.gridLayout.addWidget(self.curr_img, 1, 0, 1, 3)

        self.similar_img = QtWidgets.QLabel(self.centralwidget)
        self.similar_img.setPixmap(QtGui.QPixmap("default2.bmp"))
        self.similar_img.setScaledContents(True)
        self.similar_img.setObjectName("label")
        self.gridLayout.addWidget(self.similar_img, 2, 0, 1, 3)

        self.similar_img_metrix_label = self.get_metrix_label("default2.bmp")
        self.gridLayout.addWidget(self.similar_img_metrix_label, 1, 4)
        """
        self.change_img_btn = QtWidgets.QPushButton('change', self.centralwidget)
        self.change_img_btn.clicked.connect(self.change_img)
        self.gridLayout.addWidget(self.change_img_btn, 2, 4)
        """
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setCheckable(False)
        self.pushButton.setDefault(False)
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 4, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        self.menu_4 = QtWidgets.QMenu(self.menubar)
        self.menu_4.setObjectName("menu_4")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action_2 = QtWidgets.QAction(MainWindow)
        self.action_2.setObjectName("action_2")
        self.action_0_1 = QtWidgets.QAction(MainWindow)
        self.action_0_1.setObjectName("action_0_1")
        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_3.setObjectName("action_3")
        self.action_4 = QtWidgets.QAction(MainWindow)
        self.action_4.setObjectName("action_4")
        self.action_5 = QtWidgets.QAction(MainWindow)
        self.action_5.setObjectName("action_5")
        self.action_6 = QtWidgets.QAction(MainWindow)
        self.action_6.setObjectName("action_6")
        self.menu.addAction(self.action_3)
        self.menu.addAction(self.action_4)
        self.menu_3.addAction(self.action)
        self.menu_3.addAction(self.action_2)
        self.menu_3.addAction(self.action_0_1)
        self.menu_4.addAction(self.action_5)
        self.menu_4.addAction(self.action_6)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def change_img(self):
        if (self.similar_img.objectName() == 'label'):
            self.similar_img = QtWidgets.QLabel(self.centralwidget)
            self.similar_img.setPixmap(QtGui.QPixmap("default1.bmp"))
            self.similar_img.setScaledContents(True)
            self.similar_img.setObjectName("label1")
            self.gridLayout.addWidget(self.similar_img, 2, 0, 1, 3)
        else:
            self.similar_img = QtWidgets.QLabel(self.centralwidget)
            self.similar_img.setPixmap(QtGui.QPixmap("default2.bmp"))
            self.similar_img.setScaledContents(True)
            self.similar_img.setObjectName("label")
            self.gridLayout.addWidget(self.similar_img, 2, 0, 1, 3)

    def get_metrix_label(self, path_to_img):
        hbox = QtWidgets.QHBoxLayout()
        lbl1 = QtWidgets.QLabel('Метрика',self.centralwidget)
        value = estimate_quality(path_to_img) / 1000
        lbl2 = QtWidgets.QLabel(str(value), self.centralwidget)
        hbox.addWidget(lbl2)
        hbox.addWidget(lbl1)
        return hbox

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_2.setText(_translate("MainWindow", "Следующая пара изображений"))
        self.pushButton.setText(_translate("MainWindow", "Отметить данное изображение как лучшее"))
        self.menu.setTitle(_translate("MainWindow", "Сменить набор данных"))
        self.menu_2.setTitle(_translate("MainWindow", "Выгрузить разметку"))
        self.menu_3.setTitle(_translate("MainWindow", "Сменить режим разметки"))
        self.menu_4.setTitle(_translate("MainWindow", "Интсрукция"))
        self.action.setText(_translate("MainWindow", "Два изображения горизонтально"))
        self.action_2.setText(_translate("MainWindow", "Два изображения вертикально"))
        self.action_0_1.setText(_translate("MainWindow", "Абсолютная оценка [0,1]"))
        self.action_3.setText(_translate("MainWindow", "Загрузить выборку"))
        self.action_4.setText(_translate("MainWindow", "Выбрать из доступных"))
        self.action_5.setText(_translate("MainWindow", "Переключение между изображениями по клику"))
        self.action_6.setText(_translate("MainWindow", "Можно выбрать область содержащую объекты более низкого качества"))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())