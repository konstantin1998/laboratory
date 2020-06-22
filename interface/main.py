#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFileDialog
from interface.IQA.generated_gui import Ui_MainWindow
from interface.IQA.quality_estimator.estimator import estimate_quality
from interface.state import state


class Example(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(Example, self).__init__()
        self.setupUi(self)
        self.state = state
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
        self.action_3.setStatusTip('Выбрать директорию с изображениями')
        self.action_3.triggered.connect(self.pick_img_dir)
        self.pushButton_2.setText("Отметить нижнее как лучшее")
        self.pushButton_2.clicked.connect(self.search_lefter)
        self.pushButton.setText("Отметить верхнее как лучшее")
        self.pushButton.clicked.connect(self.search_righter)
        self.pushButton_4.clicked.connect(self.save)

        self.curr_metrix_lbl = QtWidgets.QLabel()
        self.similar_metrix_lbl = QtWidgets.QLabel()
        self.curr_img_lbl = QtWidgets.QLabel()
        self.similar_img_lbl = QtWidgets.QLabel()

        self.img_box = QVBoxLayout()
        self.gridLayout.addLayout(self.img_box, 1, 0, 2, 3)

        if self.state['path_to_unsorted_images'] == 'not_specified':
            self.show_default_img()
        else:
            self.init_comparing_imgs()

        self.show()

    def pick_img_dir(self):
        dir_name = QFileDialog.getExistingDirectory()
        self.state['path_to_unsorted_images'] = dir_name
        self.initialize_images()
        state_file = open("state.py", 'w')
        state_file.write('state=' + repr(self.state))
        state_file.close()

    def render_images(self, curr_img ={'name': 'default2.bmp', 'quality':100}, similar_img ={'name': 'default1.bmp', 'quality':100}):
        curr_img_path = os.path.join(self.state['path_to_unsorted_images'], curr_img['name'])
        similar_img_path = os.path.join(self.state['path_to_unsorted_images'], similar_img['name'])
        if (self.state['path_to_unsorted_images'] == 'not_specified'):
            curr_img_path = 'IQA/default2.bmp'
            similar_img_path = 'IQA/default1.bmp'
        self.gridLayout.removeItem(self.img_box)
        self.curr_img = QtWidgets.QLabel(self.centralwidget)
        self.curr_img.setPixmap(QtGui.QPixmap(curr_img_path))
        self.curr_img.setScaledContents(True)
        self.curr_img.setObjectName("label")
        self.img_box = QVBoxLayout()
        self.curr_img_lbl.setText('Текущее изображение: ' + curr_img['name'])
        self.img_box.addWidget(self.curr_img_lbl)
        self.img_box.addWidget(self.curr_img)
        self.curr_metrix_lbl.setText('Метрика: ' + str(curr_img['quality']))
        self.gridLayout.addWidget(self.curr_metrix_lbl, 1, 4)

        self.similar_img = QtWidgets.QLabel(self.centralwidget)
        self.similar_img.setPixmap(QtGui.QPixmap(similar_img_path))
        self.similar_img.setScaledContents(True)
        self.similar_img.setObjectName("label")
        self.similar_img_lbl.setText('Похожее изображение: ' + similar_img['name'])
        self.img_box.addWidget(self.similar_img_lbl)
        self.img_box.addWidget(self.similar_img)
        self.similar_metrix_lbl.setText('Метрика: ' + str(similar_img['quality']))
        self.gridLayout.addWidget(self.similar_metrix_lbl, 2, 4)

        self.gridLayout.addLayout(self.img_box, 1, 0, 2, 3)


    def init_comparing_imgs(self):
        curr_img = self.state['unsorted_imgs'].pop()
        if (len(self.state['sorted_imgs']) == 0):
            self.state['sorted_imgs'].append(curr_img)
            curr_img = self.state['unsorted_imgs'].pop()
        self.state['curr_img'] = curr_img
        closest_img_index = self.find_closest_img(curr_img['quality'])
        self.state['closest_img_index'] = closest_img_index

        closest_img = self.state['sorted_imgs'][closest_img_index]
        self.state['left'] = max(0, closest_img_index - int(self.state['span'] / 2)) - closest_img_index
        self.state['right'] = min(
            len(self.state['sorted_imgs']) - 1,
            closest_img_index + int(self.state['span'] / 2)) - closest_img_index
        self.state['mid'] = 0

        right_fictitious_img = {'name': 'fictitious'}
        if self.state['closest_img_index'] + self.state['right'] + 1 <= len(self.state['sorted_imgs']) - 1:
            right_fictitious_img['quality'] =\
                self.state['sorted_imgs'][self.state['closest_img_index'] + self.state['right'] + 1]['quality']
        else:
            quality_difference = 10
            right_fictitious_img['quality'] =\
                self.state['sorted_imgs'][self.state['closest_img_index'] + self.state['right']]['quality'] + 2 * quality_difference

        left_fictitious_img = {'name': 'fictitious'}
        if self.state['closest_img_index'] + self.state['left'] - 1 >= 0:
            left_fictitious_img['quality'] = \
                self.state['sorted_imgs'][self.state['closest_img_index'] + self.state['left'] - 1]['quality']
        else:
            quality_difference = 10
            left_fictitious_img['quality'] =\
                self.state['sorted_imgs'][self.state['closest_img_index'] + self.state['left']]['quality'] - 2 * quality_difference

        self.state['imgs_to_compare'] = [
            left_fictitious_img,
            *self.state['sorted_imgs'][self.state['closest_img_index'] + self.state['left']: self.state['closest_img_index'] + self.state['right'] + 1],
            right_fictitious_img]
        self.state['right'] += 1
        self.state['left'] -= 1
        self.state['right'] += abs(self.state['left'])
        self.state['mid'] += abs(self.state['left'])
        self.state['left'] += abs(self.state['left'])
        """
        closest_img_path = os.path.join(
            self.state['path_to_unsorted_images'],
            closest_img['name'])
        curr_img_path = os.path.join(
            self.state['path_to_unsorted_images'],
            curr_img['name'])
        """
        self.render_images(curr_img, closest_img)

    def search_lefter(self):
        print('search lefter')
        self.render()
        self.change_similar_img(self.state['left'], self.state['mid'])

    def search_righter(self):
        print('search righter')
        self.render()
        self.change_similar_img(self.state['mid'], self.state['right'])

    def find_closest_img(self, quality):
        def quality_func(img, param):
            return abs(img['quality'] - param)

        def get_quality_difference(img):
            return quality_func(img, quality)

        def ternarySearchMin(arr, left, right, func):
            if (left == right):
                return left
            if (abs(left - right) == 1):
                if (func(arr[left]) < func(arr[right])):
                    return left
                else:
                    return right
            if (abs(left - right) == 2):
                return left + arr[left: right + 1:1].index(min(*arr[left: right + 1:1], key=func))
            else:
                a = int((left * 2 + right) / 3)
                b = int((left + right * 2) / 3)
                if func(arr[a]) < func(arr[b]):
                    return ternarySearchMin(arr, left, b, func)
                else:
                    return ternarySearchMin(arr, a, right, func)

        if(quality < self.state['sorted_imgs'][0]['quality']):
            return 0
        if (quality > self.state['sorted_imgs'][len(self.state['sorted_imgs']) - 1]['quality']):
            return len(self.state['sorted_imgs']) - 1
        return ternarySearchMin(self.state['sorted_imgs'], 0, len(self.state['sorted_imgs']) - 1, get_quality_difference)

    def change_similar_img(self, left, right):
        curr_img = self.state['curr_img']
        mid = int((left + right) / 2)
        self.state['mid'] = mid
        if right - left == 1:
            left_img = self.state['imgs_to_compare'][left]
            right_img = self.state['imgs_to_compare'][right]
            if not ((left_img['quality'] <= curr_img['quality'] <= right_img['quality'])
            or (right_img['name'] == 'fictitious' and left_img['quality'] <= curr_img['quality'])
            or (left_img['name'] == 'fictitious' and right_img['quality'] >= curr_img['quality'])):
                curr_img['quality'] = (left_img['quality'] + right_img['quality']) / 2
            print('index to insert:', self.state['closest_img_index'] + mid + 1)
            self.state['sorted_imgs'].insert(self.state['closest_img_index'] + mid + 1, curr_img)
            self.init_comparing_imgs()
        else:
            similar_img = self.state['imgs_to_compare'][mid]
            """
            similar_img_path = os.path.join(
                self.state['path_to_unsorted_images'],
                similar_img['name'])
            curr_img_path = os.path.join(
                self.state['path_to_unsorted_images'],
                curr_img['name'])
            """
            self.render_images(curr_img, similar_img)

    def render(self):
        print('state {')
        print('    imgs to comp:', self.state['imgs_to_compare'])
        print('    left:', self.state['left'])
        print('    mid:', self.state['mid'])
        print('    right:', self.state['right'])
        print('    sorted:', self.state['sorted_imgs'])
        print('    curr:', self.state['curr_img'])
        print('}')
    def save(self):
        state_file = open("state.py", 'w')
        state_file.write('state=' + repr(self.state))
        state_file.close()

    def show_default_img(self):
        self.curr_img = QtWidgets.QLabel(self.centralwidget)
        self.curr_img.setPixmap(QtGui.QPixmap("IQA/instruction_image.png"))
        self.curr_img.setScaledContents(True)
        self.curr_img.setObjectName("label")
        self.gridLayout.addWidget(self.curr_img, 1, 0, 1, 3)
        self.specify_img_btn = QtWidgets.QPushButton("Загрузить", self)
        self.gridLayout.addWidget(self.specify_img_btn, 1, 4)
        self.specify_img_btn.clicked.connect(self.init_comparing_imgs)

    def initialize_images(self):
        try:
            image_names = os.listdir(self.state['path_to_unsorted_images'])
            for name in image_names:
                item = dict()
                item['name'] = name
                item['quality'] = estimate_quality(os.path.join(self.state['path_to_unsorted_images'], name))
                self.state['unsorted_imgs'].append(item)
        except FileNotFoundError:
            error_lbl = QtWidgets.QLabel('Неверно указана директория с изображениями')
            self.gridLayout.addWidget(error_lbl, 2, 1, 1, 3)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())