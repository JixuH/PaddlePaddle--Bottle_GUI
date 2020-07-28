### Bottle_GUI Demo 涉及到 PyQt5 及 paddlepaddle

从创建图形界面开始到最后使用infer.py完成预测

#### 1、使用 Qt Designer 设计外观

使用 `QWidget、QVBoxLayout、QHBoxLayout、QPushButton、QTabWidget、QFrame、QGraphicsBiew` 控件完成设计


![](https://ai-studio-static-online.cdn.bcebos.com/322adc5cdc47488f87f3233c2f901b3e6c7ebd488dc440a4ab5914d081bd4fef)



#### 2、使用命令：`pyuic5 -o UI.py UI.ui` 进行转换，转换成python代码


```python
# UI界面代码
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
        self.timer.timeout.connect(self.time_test) 
        self.get_camera()

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #动作
        self.start.clicked.connect(self.timer_start)
        self.stop.clicked.connect(self.timer_stop)
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
```

#### 3、写入每个按钮的功能函数

```python
# 各个功能函数

# 打开
def timer_start(self):
    print("start timer")
    self.recod_flag = False
    self.snap_flag = True
    self.timer.start(25) #设置计时间隔并启动

# 暂停
def timer_stop(self):
    print("stop timer")
    if self.recod_flag :
        self.recod_flag = False
        self.out.release()
        self.out_release_flag = False
    self.timer.stop()
    self.snap_flag = False

# 抓拍
def snap_image(self):
    tmp_time = time.localtime()
    tmp_nyr = str(tmp_time.tm_year)+str(tmp_time.tm_mon)+str(tmp_time.tm_mday)
    tmp_sfm = str(tmp_time.tm_hour)+str(tmp_time.tm_min)+str(tmp_time.tm_sec)

    if self.snap_flag:# 只有开始和录制的过程中才能抓拍
        ret, frame = self.camera.read()
        if ret:
            filename = "./" + 'img' +'.png'
            cv2.imwrite(filename, frame)

# 预测
def infer_main(self):
    os.popen("python infer.py")

# 结果
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
```
#### 在train.py 中创建记录器，记录数据，以便可视化展示
```python
# 创建记录器
log_writer = LogWriter(dir='log/', sync_cycle=10)
```

#### 4、开始训练模型

**数据集已公开，来源：自行采集、标注。 本数据集共涉及到四个品牌 --- 娃哈哈、农夫山泉、怡宝、百岁山 的水瓶数据集 数量1200张**

```python
#训练
!python faster-rcnn/train.py \
   --model_save_dir=models/ \
   --pretrained_model=imagenet_resnet50_fusebn \
   --data_dir=Bottle \
   --learning_rate=0.001 \
   --class_num=5 \
   --MASK_ON=False \
   --max_iter=20000
   ```

`VisualDL` 训练可视化的代码已经写入 `faster-rcnn` 代码包，得到的log文件夹需下载后在本地电脑查看，通过利用VisualDL进行训练可视化，可借助它进行模型的优化

在 `./log` 目录下 使用命令`visualdl --logdir=log/ --port=8080`

然后在浏览器上输入：

`http://127.0.0.1:8080`

#### 5、修改 faster-rcnn 代码中的预测图片的路径，使其与UI中的抓拍存储图像路径一致，最终结果如下图所示

![](https://ai-studio-static-online.cdn.bcebos.com/e017c62bafb84179abe6549997b0f33bc3499ae4e7ee4c02b8241bfe3f3c7f33)

![](https://ai-studio-static-online.cdn.bcebos.com/4426c30939c8455ab1337d34df3935cb36131d13ccb1431d852d1d314d6760fc)
