#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFileDialog, QDialog, QPlainTextEdit
from interface.IQA.generated_gui import Ui_MainWindow
from interface.IQA.quality_estimator.estimator import estimate_quality
from interface.state import state
from functools import partial
from PyQt5.QtCore import QRect
from interface.magnify import count_relative_pos, extract_fragment



class Example(QMainWindow, Ui_MainWindow):

    def __init__(self, state):
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
        self.action_3.triggered.connect(self.show_loading_window)
        self.pushButton_2.setText("Отметить нижнее как лучшее")
        self.pushButton_2.clicked.connect(self.search_lefter)
        self.pushButton.setText("Отметить верхнее как лучшее")
        self.pushButton.clicked.connect(self.search_righter)
        self.pushButton_4.clicked.connect(self.save)
        self.action_5.setText("Как это работает")
        self.action_5.triggered.connect(self.show_instruction)

        self.save_btn = QtWidgets.QMenu(self.menubar)
        self.save_act = QtWidgets.QAction(self)
        self.save_btn.setTitle('Сохранить')
        self.save_btn.addAction(self.save_act)
        self.menubar.addAction(self.save_btn.menuAction())
        self.save_act.setText('Сохранить')
        self.save_act.triggered.connect(self.save)

        self.curr_metrix_lbl = QtWidgets.QLabel()
        self.similar_metrix_lbl = QtWidgets.QLabel()
        self.curr_img_lbl = QtWidgets.QLabel()
        self.similar_img_lbl = QtWidgets.QLabel()
        self.img_box = QVBoxLayout()
        self.gridLayout.addLayout(self.img_box, 1, 0, 2, 3)

        self.upload_act = QtWidgets.QAction(self)
        self.upload_act.setText('Выгрузить результаты')
        self.menu_2.addAction(self.upload_act)
        self.upload_act.triggered.connect(self.upload_results)

        self.pushButton_6.clicked.connect(self.zoom)

        if self.state['path_to_unsorted_images'] == 'not_specified':
            self.show_loading_window()
        else:
            self.compare_imgs()

        self.show()

    def show_loading_window(self):
        imgs_load_window = QDialog()
        imgs_load_window.setFixedSize(QtCore.QSize(600, 400))

        progress_bar = QtWidgets.QProgressBar(imgs_load_window)
        progress_bar.setFixedSize(QtCore.QSize(300, 30))
        progress_bar.move(150, 100)

        load_imgs = partial(self.initialize_imgs, progress_bar)

        load_btn = QtWidgets.QPushButton('Загрузить')
        load_btn.clicked.connect(load_imgs)

        continue_btn = QtWidgets.QPushButton('Продолжить')
        continue_btn.clicked.connect(self.compare_imgs)
        continue_btn.clicked.connect(imgs_load_window.close)

        instruction_btn = QtWidgets.QPushButton('Инструкция')
        instruction_btn.clicked.connect(self.show_instruction)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(load_btn)
        hbox.addWidget(continue_btn)
        hbox.addWidget(instruction_btn)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.setDirection(3)

        imgs_load_window.setLayout(vbox)
        imgs_load_window.setWindowTitle("Загрузить изображения")
        imgs_load_window.setWindowModality(QtCore.Qt.ApplicationModal)
        imgs_load_window.exec_()


    def initialize_imgs(self, progress_bar):
        dir_name = QFileDialog.getExistingDirectory()
        self.state['path_to_unsorted_images'] = dir_name

        image_names = os.listdir(self.state['path_to_unsorted_images'])
        for i in range(len(image_names)):
            item = dict()
            item['name'] = image_names[i]
            self.state['loading'] = int((i + 1) / len(image_names) * 100)
            progress_bar.setProperty("value", self.state['loading'])
            item['quality'] = estimate_quality(os.path.join(self.state['path_to_unsorted_images'], image_names[i]))
            self.state['unsorted_imgs'].append(item)

        state_file = open("state.py", 'w')
        state_file.write('state=' + repr(self.state))
        state_file.close()

    def upload_results(self):
        dir_name = QFileDialog.getExistingDirectory()
        results_path = os.path.join(dir_name, 'results.py')
        results_file = open(results_path, 'w')
        results_file.write(repr(self.state['sorted_imgs']))
        results_file.close()

    def show_uploading_window(self):
        uploading_winow = QDialog()
        uploading_winow.setFixedSize(QtCore.QSize(400, 150))

        lbl = QtWidgets.QPushButton('Выберите директорию для загрузки результатов', uploading_winow)
        lbl.move(160, 50)

        pick_btn = QtWidgets.QPushButton('Выбрать директорию', uploading_winow)
        pick_btn.move(160, 70)
        pick_btn.clicked.connect(self.upload_results)

        uploading_winow.setWindowTitle("Выгрузить изображения")
        uploading_winow.exec_()

    def render_images(self, curr_img={'name': 'default2.bmp', 'quality':100}, similar_img={'name': 'default1.bmp', 'quality':100}):
        curr_img_path = os.path.join(self.state['path_to_unsorted_images'], curr_img['name'])
        similar_img_path = os.path.join(self.state['path_to_unsorted_images'], similar_img['name'])
        self.state['similar_img'] = similar_img
        if (self.state['path_to_unsorted_images'] == 'not_specified'):
            curr_img_path = 'IQA/images/default2.bmp'
            similar_img_path = 'IQA/images/default1.bmp'
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

    def compare_imgs(self):
        self.dataset_load_pb.setProperty(
            "value",
            int(len(self.state['sorted_imgs']) * 100 / (len(self.state['sorted_imgs']) + len(self.state['unsorted_imgs'])))
        )
        if len(self.state['unsorted_imgs']) != 0:
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
                right_fictitious_img['quality'] = \
                    self.state['sorted_imgs'][self.state['closest_img_index'] + self.state['right'] + 1]['quality']
            else:
                quality_difference = 10
                right_fictitious_img['quality'] = \
                    self.state['sorted_imgs'][self.state['closest_img_index'] + self.state['right']]['quality'] + 2 * quality_difference

            left_fictitious_img = {'name': 'fictitious'}
            if self.state['closest_img_index'] + self.state['left'] - 1 >= 0:
                left_fictitious_img['quality'] = \
                    self.state['sorted_imgs'][self.state['closest_img_index'] + self.state['left'] - 1]['quality']
            else:
                quality_difference = 10
                left_fictitious_img['quality'] = \
                    self.state['sorted_imgs'][self.state['closest_img_index'] + self.state['left']]['quality'] - 2 * quality_difference

            self.state['imgs_to_compare'] = [
                left_fictitious_img,
                *self.state['sorted_imgs'][self.state['closest_img_index'] + self.state['left']: self.state['closest_img_index'] + self.state['right'] + 1],
                right_fictitious_img]
            self.state['right'] += 1
            self.state['left'] -= 1
            margin = abs(self.state['left'])
            self.state['right'] += margin
            self.state['mid'] += margin
            self.state['left'] += margin
            self.state['margin'] = margin

            self.render_images(curr_img, closest_img)
        else:
            self.save()
            self.pushButton_2.disconnect()
            self.pushButton.disconnect()
            self.show_closing_window()

    def show_instruction(self):
        instruction = QDialog()
        instruction.text_area = QPlainTextEdit(instruction)
        instruction.text_area.insertPlainText('Нажмите "Загрузить" для того, чтобы выбрать директорию с изображениями.'
                                              ' Загрузка может занять продолжительное время. Дождитесь окончания загрузки'
                                              ' и нажмите "Продолжить". После этого выпопадете в главное окно программы. '
                                              'Вверху располагается текущее изображение под ним - похожее по качеству '
                                              'изображение. Справа от изображений написаны метрики качества, посчитанные '
                                              'автоматически. Вам нужно выбрать лучшее, исходя из субъективных представлений.'
                                              ' Когда все изображения обработаны автоматически всплывет соответствующее окно.'
                                              ' При нажатии на кнопку "ок" результаты сортировки изображений загрузятся в файл,'
                                              ' который надо будет выбрать и программа закроется. Если нужно еще отсортировать'
                                              ' изображения, надо нажать на кнопку "Сортировать еще", чтобы загрузить'
                                              ' изображения заново и начать сортировать. \n')
        instruction.text_area.move(10,10)
        instruction.text_area.resize(400,200)
        instruction.text_area.setDisabled(True)
        instruction.setWindowTitle('Инструкция')

        instruction.exec_()

    def show_closing_window(self):
        closing_window = QDialog()
        closing_window.setFixedSize(QtCore.QSize(400, 150))

        cancel_btn = QtWidgets.QPushButton("ok", closing_window)
        cancel_btn.move(170, 60)
        cancel_btn.clicked.connect(self.save)
        cancel_btn.clicked.connect(self.close)
        cancel_btn.clicked.connect(closing_window.close)

        lbl = QtWidgets.QLabel('Изображения отсортированы. Нажмите "ok" для завершения программы', closing_window)
        lbl.move(20, 30)

        continue_btn = QtWidgets.QPushButton('Сортировать ещё', closing_window)
        continue_btn.clicked.connect(self.state_to_default)
        continue_btn.clicked.connect(self.close)
        continue_btn.clicked.connect(self.show_loading_window)
        continue_btn.clicked.connect(closing_window.close)
        continue_btn.move(165, 85)

        upload_btn = QtWidgets.QPushButton('Выгрузить результаты', closing_window)
        upload_btn.clicked.connect(self.upload_results)
        upload_btn.clicked.connect(self.state_to_default)
        upload_btn.move(150, 110)

        closing_window.setWindowTitle("Изображения отсортированы")
        closing_window.setWindowModality(QtCore.Qt.ApplicationModal)
        closing_window.exec_()

    def search_lefter(self):
        self.change_similar_img(self.state['left'], self.state['mid'])

    def search_righter(self):
        self.change_similar_img(self.state['mid'], self.state['right'])

    def zoom(self):
        self.state['zoommed'] = True

    def find_closest_img(self, quality):
        def f(number, x):
            return abs(x['quality'] - number)

        get_quality_difference = partial(f, quality)

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
            or (left_img['name'] == 'fictitious' and left_img['quality'] >= curr_img['quality'])
            or (right_img['name'] == 'fictitious' and right_img['quality'] <= curr_img['quality'])):
                curr_img['quality'] = int((left_img['quality'] + right_img['quality']) / 2)
            self.state['sorted_imgs'].insert(self.state['closest_img_index'] + right - self.state['margin'], curr_img)
            self.compare_imgs()
        else:
            similar_img = self.state['imgs_to_compare'][mid]
            self.render_images(curr_img, similar_img)

    def render(self):
        print('state {')
        print('    imgs to comp:', self.state['imgs_to_compare'])
        print('    left:', self.state['left'])
        print('    mid:', self.state['mid'])
        print('    right:', self.state['right'])
        print('    sorted:', self.state['sorted_imgs'])
        print('    closest img:', self.state['closest_img_index'])
        print('    curr:', self.state['curr_img'])
        print('}')

    def save(self):
        #self.state['unsorted_imgs'].append(self.state['curr_img'])
        state_file = open("state.py", 'w')
        state_file.write('state=' + repr(self.state))
        state_file.close()

    def state_to_default(self):
        self.state['path_to_unsorted_images'] = 'not_specified'
        self.state['output_dir'] = 'not_specified'
        self.state['unsorted_imgs'] = []
        self.state['sorted_imgs'] = []

    def magnify(self):
        magnifier_window = QDialog()

        curr_cropped_path = self.state['curr_img_cropped']
        curr_img_cropped = QtWidgets.QLabel(magnifier_window)
        curr_img_cropped.setPixmap(QtGui.QPixmap(curr_cropped_path))
        curr_img_lbl = QtWidgets.QLabel(magnifier_window)
        curr_img_lbl.setText('Текущее')

        similar_cropped_path = self.state['similar_img_cropped']
        similar_img_cropped = QtWidgets.QLabel(magnifier_window)
        similar_img_cropped.setPixmap(QtGui.QPixmap(similar_cropped_path))
        similar_img_lbl = QtWidgets.QLabel(magnifier_window)
        similar_img_lbl.setText('Похожее')

        grid = QtWidgets.QGridLayout()
        magnifier_window.setLayout(grid)

        grid.addWidget(curr_img_lbl, 1, 1)
        grid.addWidget(curr_img_cropped, 1, 2)
        grid.addWidget(similar_img_lbl, 2, 1)
        grid.addWidget(similar_img_cropped, 2, 2)

        magnifier_window.setGeometry(300, 300, 300, 300)
        magnifier_window.setFixedSize(QtCore.QSize(300, 300))
        magnifier_window.setWindowTitle('Images')
        magnifier_window.setWindowModality(QtCore.Qt.ApplicationModal)
        magnifier_window.exec_()

    def mousePressEvent(self, event):

        if self.state['zoommed']:
            self.state['zoommed'] = False
            curr_img_top_left = self.curr_img.pos() + self.centralwidget.pos()
            similar_img_top_left = self.similar_img.pos() + self.centralwidget.pos()
            curr_img_rect = QRect(curr_img_top_left, self.curr_img.rect().size())
            similar_img_rect = QRect(similar_img_top_left, self.similar_img.rect().size())

            if (curr_img_rect.contains(event.pos()) or  similar_img_rect.contains(event.pos())):
                relative_pos = (0, 0)
                curr_img_path = os.path.join(self.state['path_to_unsorted_images'], self.state['curr_img']['name'])
                similar_img_path = os.path.join(self.state['path_to_unsorted_images'], self.state['similar_img']['name'])
                if curr_img_rect.contains(event.pos()):
                    relative_pos = count_relative_pos(curr_img_rect, event.pos())
                if similar_img_rect.contains(event.pos()):
                    relative_pos = count_relative_pos(similar_img_rect, event.pos())

                extract_fragment(curr_img_path, self.state['curr_img_cropped'], relative_pos)
                extract_fragment(similar_img_path, self.state['similar_img_cropped'], relative_pos)
                self.magnify()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example(state)
    sys.exit(app.exec_())