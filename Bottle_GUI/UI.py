# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar 
import cv2
import time
import os
import numpy as np
from PyQt5.QtWidgets import QGraphicsView

def cv_imread(file_path):
    cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
    return cv_img

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1092, 730)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.shoot = QtWidgets.QWidget()
        self.shoot.setObjectName("shoot")
        self.gridLayout = QtWidgets.QGridLayout(self.shoot)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(self.shoot)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.figure, self.figaxes = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self.frame)
        self.gridLayout.addWidget(self.toolbar)
        self.gridLayout.addWidget(self.canvas)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        self.tabWidget.addTab(self.shoot, "")
        self.infer_2 = QtWidgets.QWidget()
        self.infer_2.setObjectName("infer_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.infer_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.result_2 = QtWidgets.QGraphicsView(self.infer_2)
        self.result_2.setObjectName("result_2")
        self.gridLayout_2.addWidget(self.result_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.infer_2, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.start = QtWidgets.QPushButton(self.centralwidget)
        self.start.setObjectName("start")
        self.horizontalLayout.addWidget(self.start)
        self.stop = QtWidgets.QPushButton(self.centralwidget)
        self.stop.setObjectName("stop")
        self.horizontalLayout.addWidget(self.stop)
        self.snap = QtWidgets.QPushButton(self.centralwidget)
        self.snap.setObjectName("snap")
        self.horizontalLayout.addWidget(self.snap)
        self.infer = QtWidgets.QPushButton(self.centralwidget)
        self.infer.setObjectName("infer")
        self.horizontalLayout.addWidget(self.infer)
        self.result = QtWidgets.QPushButton(self.centralwidget)
        self.result.setObjectName("result")
        self.horizontalLayout.addWidget(self.result)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1092, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.time_test) #计时结束调用方法
        self.get_camera()

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #动作
        self.start.clicked.connect(self.timer_start)
        self.stop.clicked.connect(self.timer_stop)
        # self.recod.clicked.connect(self.recod_image)
        self.snap.clicked.connect(self.snap_image)
        self.infer.clicked.connect(self.infer_main)
        self.result.clicked.connect(self.ImageShow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "目标检测Demo")) 
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.shoot), _translate("MainWindow", "拍摄"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.infer_2), _translate("MainWindow", "预测"))
        self.start.setText(_translate("MainWindow", "打开"))
        self.stop.setText(_translate("MainWindow", "暂停"))
        self.snap.setText(_translate("MainWindow", "抓拍"))
        self.infer.setText(_translate("MainWindow", "预测"))
        self.result.setText(_translate("MainWindow", "结果"))

    def get_camera(self):
        self.camera = cv2.VideoCapture(0)
        self.camera.set(4,720)

    def time_test(self):
        ret, frame = self.camera.read()
        if ret:
            if self.recod_flag :
                # frame = cv2.flip(frame, 1)# 在帧上进行操作 左右翻转了
                self.out.write(frame) # 保存视频

            b, g, r = cv2.split(frame)
            self.img2 = cv2.merge([r,g,b])# opencv和matplotlib的图像rgb顺序不一样

            self.figaxes.clear()
            self.figaxes.imshow(self.img2)
            # self.figaxes.autoscale_view()
            self.figure.canvas.draw()
        else:
            print("read camera error")

    def timer_start(self):
        print("start timer")
        self.recod_flag = False
        self.snap_flag = True
        self.timer.start(25) #设置计时间隔并启动

    def timer_stop(self):
        print("stop timer")
        if self.recod_flag :
            self.recod_flag = False
            self.out.release()
            self.out_release_flag = False
        self.timer.stop()
        self.snap_flag = False

    def snap_image(self):
        tmp_time = time.localtime()
        tmp_nyr = str(tmp_time.tm_year)+str(tmp_time.tm_mon)+str(tmp_time.tm_mday)
        tmp_sfm = str(tmp_time.tm_hour)+str(tmp_time.tm_min)+str(tmp_time.tm_sec)

        if self.snap_flag:# 只有开始和录制的过程中才能抓拍
            ret, frame = self.camera.read()
            if ret:
                filename = "./" + 'img' +'.png'
                cv2.imwrite(filename, frame)

    def ImageShow(self):
        AbsolutePath="./img.png"
        img = cv_imread(AbsolutePath)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB,img)
        x = img.shape[1]#获取图像宽度
        y = img.shape[0]#获取图像高度
        frame = QtGui.QImage(img.data, x, y, x*3, QtGui.QImage.Format_RGB888)

        pix = QtGui.QPixmap.fromImage(frame)
        self.item=QtWidgets.QGraphicsPixmapItem(pix)#创建像素图元
        self.scene=QtWidgets.QGraphicsScene()#创建场景
        self.scene.clear()
        self.scene.addItem(self.item)
        self.scene.update()
        self.result_2.setScene(self.scene)  # 将场景添加至视图

    def infer_main(self):
        os.popen("python infer.py")

