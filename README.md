# PaddlePaddle--Bottle_GUI
运行 UI_main.py
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200727190450654.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQyNTQ5NjEy,size_16,color_FFFFFF,t_70)

五个按钮功能分别为打开摄像头、暂停影像、抓拍图像、对图像进行预测、读取结果并展示

```python
# 动作
self.start.clicked.connect(self.timer_start)
self.stop.clicked.connect(self.timer_stop)
self.snap.clicked.connect(self.snap_image)
self.infer.clicked.connect(self.infer_main)
self.result.clicked.connect(self.ImageShow)
```

预测结果如下图所示：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200727191502405.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQyNTQ5NjEy,size_16,color_FFFFFF,t_70)
