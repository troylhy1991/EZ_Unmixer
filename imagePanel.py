from PyQt4.QtGui import *
from PyQt4.QtCore import *

import QImageConverter as QC
import copy

class ImagePanel(QFrame):
    def __init__(self,image):
        super(ImagePanel, self).__init__()

        self.drawState = 0
        self.drawingRect = 0
        self.x = 10
        self.y = 10

        self.begin = QPoint()
        self.end = QPoint()

        self.Height, self.Width = image.shape
        self.image = QC.numpy2qimage(image)

        self.imageLabel = QLabel()
        self.scrollArea = QScrollArea()

        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored,QSizePolicy.Ignored)
        self.imageLabel.setMouseTracking(True)
        self.imageLabel.setScaledContents(True)

        pic = QImage(self.Width, self.Height, QImage.Format_ARGB32_Premultiplied)
        pic.fill(qRgb(0,0,0))
        painter = QPainter(pic)
        painter.setCompositionMode(QPainter.CompositionMode_Plus)

        channelImage = QImage(self.Width, self.Height, QImage.Format_ARGB32_Premultiplied)
        channelImage.fill(qRgb(255,255,255))
        channelImage.setAlphaChannel(self.image)
        painter.drawImage(0,0,channelImage)

        del painter

        self.imageLabel.setPixmap(QPixmap.fromImage(pic))

        self.scrollArea.setMouseTracking(True)
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.horizontalScrollBar().setRange(0,2048)
        self.scrollArea.verticalScrollBar().setRange(0,2048)
        self.scrollArea.horizontalScrollBar().setValue(0)
        self.scrollArea.verticalScrollBar().setValue(0)
        #self.scrollArea.setWidgetResizable(True)
        #self.scrollArea.setFixedSize(1026,1026)
        self.scrollArea.setFixedSize(800,800)

        self.setMouseTracking(True)
        HBoxLayout = QHBoxLayout()
        HBoxLayout.addWidget(self.scrollArea)
        self.setLayout(HBoxLayout)

    def refreshImage(self,image):
        self.image_np = image
        self.image = QC.numpy2qimage(self.image_np)

        pic = QImage(self.Width, self.Height, QImage.Format_ARGB32_Premultiplied)
        pic.fill(qRgb(0,0,0))
        painter = QPainter(pic)
        painter.setCompositionMode(QPainter.CompositionMode_Plus)

        channelImage = QImage(self.Width, self.Height, QImage.Format_ARGB32_Premultiplied)
        channelImage.fill(qRgb(255,255,255))
        channelImage.setAlphaChannel(self.image)
        painter.drawImage(0,0,channelImage)
        #painter.drawImage(0,0,self.image)

        pen = QPen(Qt.red)
        painter.setPen(pen)

        for i in range(-10,11):
            for j in range(-10,11):
                if i == j or i == -j:
                    painter.drawPoint(i+self.x, j +self.y)

        #print(self.drawState)
        if self.drawState == 1:
            pen.setColor(Qt.white)
            painter.setPen(pen)
            for i in range(0,self.Height):
                painter.drawPoint(self.x, i)
            for j in range(0,self.Width):
                painter.drawPoint(j, self.y)


            if self.drawingRect == 1:
                br = QBrush(QColor(100, 10, 10, 40))
                painter.setBrush(br)
                painter.drawRect(QRect(self.begin, self.end))

                del br
        del pen
        del painter

        self.pixmap = QPixmap.fromImage(pic)

        self.imageLabel.setPixmap(self.pixmap)

    def paintEvent(self, event):
        return 0

    def keyPressEvent(self, e):

        if (e.key() == Qt.Key_D):
            self.emit(SIGNAL("KEY_D_Pressed"))

        #self.refreshImage()

    def mouseMoveEvent(self, event):
        self.x = event.pos().x() + self.scrollArea.horizontalScrollBar().value() -10
        self.y = event.pos().y() + self.scrollArea.verticalScrollBar().value() -10



        end_x = event.pos().x() + self.scrollArea.horizontalScrollBar().value() - 10
        end_y = event.pos().y() + self.scrollArea.verticalScrollBar().value() - 10
        self.end = QPoint(end_x, end_y)

        self.emit(SIGNAL("mouseMoveEvent"), self.x, self.y)
        #self.update()


    def mousePressEvent(self, event):
        begin_x = event.pos().x() + self.scrollArea.horizontalScrollBar().value() - 10
        begin_y = event.pos().y() + self.scrollArea.verticalScrollBar().value() - 10
        self.begin = QPoint(begin_x, begin_y)
        end_x = event.pos().x() + self.scrollArea.horizontalScrollBar().value() - 10
        end_y = event.pos().y() + self.scrollArea.verticalScrollBar().value() - 10
        self.end = QPoint(end_x, end_y)

        self.drawingRect = 1
        if self.drawState == 1:
            self.emit(SIGNAL("NewRectStart"), self.begin, self.end)
        #self.update()


    def mouseReleaseEvent(self, event):
        end_x = event.pos().x() + self.scrollArea.horizontalScrollBar().value() - 10
        end_y = event.pos().y() + self.scrollArea.verticalScrollBar().value() - 10
        self.end = QPoint(end_x, end_y)
        self.drawingRect = 0

        if self.drawState == 1:
            self.emit(SIGNAL("NewRectGenerated"), self.begin, self.end)
        #self.update()
