import pims
import tifffile as tiff

import sys
import numpy as np
import random

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from adjust import *
from imagePanel import *
from table import *
from popup import *



class Unmixer(QMainWindow):
    def __init__(self):
        super(Unmixer, self).__init__()

        ################################## Initialize Variables ###################################
        self.image16_master_org = []
        self.image8_master_org = []
        self.image8_master_update = []
        self.frames_master = 0


        self.image16_leak_org = []
        self.image16_leak_update = []
        self.image8_leak_org = []
        self.image8_leak_update = []
        self.frames_leak = 0

        self.t = 0

        self.N = 0
        self.ratio = 0
        self.area_list = []
        self.intensity_master_list=[]
        self.intensity_leak_list = []
        self.ratio_list = []
        self.x_s_list = []
        self.y_s_list = []
        self.x_l_list = []
        self.y_l_list = []

        ################################## Menu Setup #############################################

        self.statusBar()

        # File Menu
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
    	exitAction.setStatusTip('Exit application')
    	exitAction.triggered.connect(qApp.quit)

        loadMasterImageAction = QAction('&Load Master Images', self)
        loadMasterImageAction.triggered.connect(self.loadMasterImage)

        loadLeakImageAction = QAction('&Load Leaked Images', self)
        loadLeakImageAction.triggered.connect(self.loadLeakImage)

        saveUnmixedImageAction = QAction('&Save Unmixed Images', self)
        saveUnmixedImageAction.triggered.connect(self.saveUnmixedImage)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(loadMasterImageAction)
        fileMenu.addAction(loadLeakImageAction)
        fileMenu.addAction(saveUnmixedImageAction)
        fileMenu.addAction(exitAction)

        # Operation Menu

        opsMenu = menubar.addMenu('Operations')

        leakRatioAction = QAction('Spectral Leakage Ratio',self)
        leakRatioAction.triggered.connect(self.leakRatio)

        setLeakRatioAction = QAction('Set Leakage Ratio', self)
        setLeakRatioAction.triggered.connect(self.setLeakRatio)

        adjustAction = QAction('Contrast/Brightness', self)
        adjustAction.triggered.connect(self.adjustContrastBrightness)

        viewSampleHistoryAction = QAction('View Sample History',self)
        viewSampleHistoryAction.triggered.connect(self.viewSampleHistory)

        resetAction = QAction('Reset Sample History', self)
        resetAction.triggered.connect(self.resetSample)

        dequeueSampleAction = QAction('Remove Most Recent Sample', self)
        dequeueSampleAction.triggered.connect(self.DQSample)

        unmixAction = QAction('Unmix', self)
        unmixAction.triggered.connect(self.unmix)

        opsMenu.addAction(leakRatioAction)
        opsMenu.addAction(setLeakRatioAction)
        opsMenu.addAction(adjustAction)
        opsMenu.addAction(viewSampleHistoryAction)
        opsMenu.addAction(resetAction)
        opsMenu.addAction(dequeueSampleAction)
        opsMenu.addAction(unmixAction)

    	# Help Menu
    	helpMenu = menubar.addMenu('&Help')

    	aboutAction = QAction('&About',self)
    	aboutAction.triggered.connect(self.about_func)

    	helpMenu.addAction(aboutAction)

        ###################################### ImagePanel Setup ####################################
        tempImage = np.zeros((2048,2048))
        self.image_master = ImagePanel(tempImage)
        self.image_leak = ImagePanel(tempImage)



        HBoxLayout = QHBoxLayout()
        HBoxLayout.addWidget(self.image_master)
        HBoxLayout.addWidget(self.image_leak)

        self.pixelInfo = QLabel("x: ; y: ; ")

        VBoxLayout = QVBoxLayout()
        VBoxLayout.addLayout(HBoxLayout)
        VBoxLayout.addWidget(self.pixelInfo)

        self.establishConnections()
        window = QWidget()
        window.setLayout(VBoxLayout)
        self.setCentralWidget(window)
        self.setWindowTitle('EZ Unmixer 1.0')
        self.show()

    ########################################## slot function ########################################
    def about_func(self):
    	QMessageBox.information(self,"About","Version: EZ Unmixer 1.0 \n Author: Hengyang Lu \n Email: hlu9@uh.edu \n Copy Right Reserved.")

    def loadMasterImage(self):

        self.image_master_path = str(QFileDialog.getOpenFileName(self,"Select Master Image"))
        self.image16_master_org = pims.open(self.image_master_path)

        h,w= self.image16_master_org[0].shape
        self.frames_master = len(self.image16_master_org[0])

        self.image16_master_background = np.mean(np.array(self.image16_master_org[0]))


        self.image8_master_org = self.img16to8(self.image16_master_org[0])
        self.image_master.refreshImage(self.image8_master_org)
        self.image8_master_update = np.array(self.image8_master_org)
        self.t = 0

    def loadLeakImage(self):
        self.image_leak_path = str(QFileDialog.getOpenFileName(self,"Select Leak Image"))
        self.image16_leak_org = pims.open(self.image_leak_path)

        h,w= self.image16_leak_org[0].shape
        self.frames_leak = len(self.image16_leak_org[0])


        self.image8_leak_org = self.img16to8(self.image16_leak_org[0])
        self.image_leak.refreshImage(self.image8_leak_org)
        self.t = 0

        self.image16_leak_update = np.array(self.image16_leak_org[0])
        self.image16_leak_background = np.mean(self.image16_leak_update)
        self.image8_leak_update = np.array(self.image8_leak_org)

    def saveUnmixedImage(self):
        name = QFileDialog.getSaveFileName(self, 'Save Unmixed Image')
        name = str(name)
        output = np.array(self.image16_leak_update, dtype = np.uint16)
        tiff.imsave(name, output)


    def adjustContrastBrightness(self):
    	self.adjust = Adjust()
    	self.adjust.show()

        self.connect(self.adjust, SIGNAL("IMAGEADJUST"), self.adjustslot)
        self.adjust.Button.clicked.connect(self.resetImages)

    def resetImages(self):
        if str(self.adjust.combo.currentText()) == "CH_Master":
            self.image8_master_update = np.array(self.image8_master_org)
            self.image_master.refreshImage(self.image8_master_update)

        if str(self.adjust.combo.currentText()) == "CH_Leakage":
            self.image8_leak_update = np.array(self.image8_leak_org)
            self.image_leak.refreshImage(self.image8_leak_update)

    def leakRatio(self):
        QMessageBox.information(self,"Spectral Leakage Ratio", "{0:.4f}".format(self.ratio))

    def viewSampleHistory(self):
        tabledata = []
        for i in range(0,self.N):
            temp = []
            temp.append(str(i+1))
            temp.append(str(self.x_s_list[i]))
            temp.append(str(self.y_s_list[i]))
            temp.append(str(self.x_l_list[i]))
            temp.append(str(self.x_l_list[i]))
            temp.append(str(self.area_list[i]))
            temp.append(str(self.intensity_master_list[i]))
            temp.append(str(self.intensity_leak_list[i]))
            temp.append(str(self.ratio_list[i]))
            tabledata.append(temp)

        self.table = Table(tabledata)
        self.table.show()

    def resetSample(self):
        self.N = 0
        self.ratio = 0
        self.area_list = []
        self.intensity_master_list=[]
        self.intensity_leak_list = []
        self.ratio_list = []
        self.x_s_list = []
        self.y_s_list = []
        self.x_l_list = []
        self.y_l_list = []

    def DQSample(self):
        self.N = self.N - 1
        self.x_s_list = self.x_s_list[:-1]
        self.y_s_list = self.y_s_list[:-1]
        self.x_l_list = self.x_l_list[:-1]
        self.y_l_list = self.y_l_list[:-1]
        self.area_list = self.area_list[:-1]
        self.intensity_master_list = self.intensity_master_list[:-1]
        self.intensity_leak_list = self.intensity_leak_list[:-1]
        self.ratio_list = self.ratio_list[:-1]
        self.ratio = np.mean(self.ratio_list)

    def setLeakRatio(self):
        self.popup = MyPopup()
        self.connect(self.popup, SIGNAL("SET_RATIO"), self.setRatioSlot)

    def setRatioSlot(self, ratio):
        self.ratio = ratio
        print(ratio)

        self.popup.deleteLater()


    def unmix(self):
        self.image16_leak_update = self.image16_leak_update - np.array(self.image16_master_org[0]) * self.ratio
        self.image16_leak_update[self.image16_leak_update<0] = 0

        self.image8_leak_org = self.img16to8(self.image16_leak_update)
        self.image8_leak_update = self.image8_leak_org
        self.image_leak.refreshImage(self.image8_leak_org)

    ########################################## In and Out ###########################################
    def establishConnections(self):
        self.image_master.scrollArea.horizontalScrollBar().valueChanged.connect(self.image_master_hbar_value_change)
        self.image_master.scrollArea.verticalScrollBar().valueChanged.connect(self.image_master_vbar_value_change)

        self.image_leak.scrollArea.horizontalScrollBar().valueChanged.connect(self.image_leak_hbar_value_change)
        self.image_leak.scrollArea.verticalScrollBar().valueChanged.connect(self.image_leak_vbar_value_change)

        self.connect(self.image_master, SIGNAL("mouseMoveEvent"), self.updatePixelInfo)
        self.connect(self.image_leak, SIGNAL("mouseMoveEvent"), self.updatePixelInfo)

        self.connect(self.image_master, SIGNAL("KEY_D_Pressed"), self.updateDrawState)
        self.connect(self.image_leak, SIGNAL("KEY_D_Pressed"), self.updateDrawState)

        self.connect(self.image_master, SIGNAL("NewRectStart"), self.updateRectStart)
        self.connect(self.image_leak, SIGNAL("NewRectStart"), self.updateRectStart)

        self.connect(self.image_master, SIGNAL("NewRectGenerated"), self.updateRectRelease)
        self.connect(self.image_leak, SIGNAL("NewRectGenerated"), self.updateRectRelease)


    # signal from adjust
    def adjustslot(self, lower, upper, brightness, contrast, channel):
        # Modify something with self.image8_master_update   <--- self.image8_master_org
        # Modify something with self.image8_leak_update    <--- self.image8_leak-org

        if channel == "CH_Master":
            self.image8_master_update = self.image8_master_update.astype('int16')
            self.image8_master_update = self.image8_master_org + brightness*5

            self.image8_master_update[self.image8_master_update < lower] = 0
            self.image8_master_update[self.image8_master_update > upper] = 255

            self.image8_master_update = self.image8_master_update.astype('uint8')
            self.image_master.refreshImage(self.image8_master_update)

        if channel == "CH_Leakage":
            self.image8_leak_update = self.image8_leak_update.astype('int16')
            self.image8_leak_update = self.image8_leak_org + brightness*5

            self.image8_leak_update[self.image8_leak_update < lower] = 0
            self.image8_leak_update[self.image8_leak_update > upper] = 255

            self.image8_leak_update = self.image8_leak_update.astype('uint8')
            self.image_leak.refreshImage(self.image8_leak_update)




    # signal from imagePanel Left
    def image_master_hbar_value_change(self):
        offset = self.image_master.scrollArea.horizontalScrollBar().value()
        self.image_leak.scrollArea.horizontalScrollBar().setValue(offset)

    def image_master_vbar_value_change(self):
        offset = self.image_master.scrollArea.verticalScrollBar().value()
        self.image_leak.scrollArea.verticalScrollBar().setValue(offset)

    def image_leak_hbar_value_change(self):
        offset = self.image_leak.scrollArea.horizontalScrollBar().value()
        self.image_master.scrollArea.horizontalScrollBar().setValue(offset)

    def image_leak_vbar_value_change(self):
        offset = self.image_leak.scrollArea.verticalScrollBar().value()
        self.image_master.scrollArea.verticalScrollBar().setValue(offset)

    def updatePixelInfo(self, x, y):
        info_text = "x: " + str(x) +"; " + "y: " + str(y) + "; " + "master intensity: " + str(self.image16_master_org[0][y][x]) + "; " + "leak intensity: " + str(self.image16_leak_org[0][y][x]) + "; "

        self.image_master.x0 = self.image_master.x
        self.image_leak.x0 = self.image_leak.x
        self.image_master.y0 = self.image_master.y
        self.image_leak.y0 = self.image_leak.y

        self.image_master.x = x
        self.image_leak.x = x
        self.image_master.y = y
        self.image_leak.y = y

        self.pixelInfo.setText(info_text)

        if (self.image_master.x0 == x and self.image_master.y0 == y) or (self.image_leak.x0 == x and self.image_leak.y0 == y):
            self.image_master.refreshImage(self.image8_master_update)
            self.image_leak.refreshImage(self.image8_leak_update)
        #self.image_master.refreshImage2()
        #self.image_leak.refreshImage2()

        self.image_master.end = QPoint(x,y)
        self.image_leak.end = QPoint(x,y)

    def updateDrawState(self):

        if self.image_master.drawState == 0:
            self.image_master.drawState = 1
        else:
            self.image_master.drawState = 0

        if self.image_leak.drawState == 0:
            self.image_leak.drawState = 1
        else:
            self.image_leak.drawState = 0

        print("master " + str(self.image_master.drawState))
        print("leak " + str(self.image_leak.drawState))

    def updateRectStart(self,begin, end):
        self.image_master.begin = begin
        self.image_master.end = end

        self.image_leak.begin = begin
        self.image_leak.end = end

        self.image_master.drawingRect = 1
        self.image_leak.drawingRect = 1

    def updateRectRelease(self, begin, end):
        #self.image_master.begin = begin
        self.image_master.end = end

        #self.image_leak.begin = begin
        self.image_leak.end = end

        self.image_master.drawingRect = 0
        self.image_leak.drawingRect = 0

        # New Rectangle added, so we will maintain a queue of Sampled area
        # Index  x_tl  y_tl  x  y  area  intensity_master intensity_leak  ratio
        # Calculate avg_ratio
        x1 = begin.x()
        y1 = begin.y()

        x2 = end.x()
        y2 = end.y()

        if x1 > x2:
            x = x1
            x1 = x2
            x2 = x
        if y1 > y2:
            y = y1
            y1 = y2
            y2 = y
        area = (x2-x1)*(y2-y1)
        print("area: " + str(area))
        intensity_master = float(self.image16_master_org[0][y1:y2,x1:x2].sum())/float(area)
        intensity_leak = float(self.image16_leak_org[0][y1:y2,x1:x2].sum())/float(area)
        print("intensity master" + str(intensity_master))
        print("intensity leak" + str(intensity_leak))
        ratio = (intensity_leak-self.image16_leak_background)/(intensity_master-self.image16_master_background)


        self.area_list.append(area)
        self.ratio_list.append(ratio)
        self.x_s_list.append(x1)
        self.y_s_list.append(y1)
        self.x_l_list.append(x2)
        self.y_l_list.append(y2)
        self.N = len(self.ratio_list)
        self.ratio = np.mean(self.ratio_list)
        self.intensity_master_list.append(intensity_master)
        self.intensity_leak_list.append(intensity_leak)

    # signal from imagePanel Right


    ########################################## helper function ######################################
    def img16to8(self, image):
        # get the maximum value of current frame
        # max --> 255; 50 --> 0; the other --> linear interpolation
        #maxvalue = max(image.flatten())
        image = np.array(image)
        maxvalue = 0.1 * np.max(image)
        if maxvalue > 2000:
            maxvalue = 2000

        image[image>maxvalue] = maxvalue
        # maxvalue = 2000
        # h, w = image.shape
        # image8 = np.zeros((h,w), dtype = np.uint8)

        image0 = (image - 0) * 255.0 / (maxvalue-0)
        image0[image0 > 255] = 255
        image0[image0 < 0] = 0

        image0 = np.array(image0)

        image8 = image0.astype('uint8')

        #image8 = np.uint8()
        #image8[image8 > 255] = 255
        #image8[image8 < 0] = 0

        return image8



    def imadjust(img, tol=[0.01, 0.99]):
        # img : input one-layer image (numpy array)
        # tol : tolerance, from 0 to 1.

        assert len(img.shape) == 2, 'Input image should be 2-dims'

        if img.dtype == 'uint8':
            nbins = 255
        elif img.dtype == 'uint16':
            nbins = 65535

        N = np.histogram(img, bins=nbins, range=[0, nbins])  # get histogram of image
        cdf = np.cumsum(N[0]) / np.sum(N[0])  # calculate cdf of image
        ilow = np.argmax(cdf > tol[0]) / nbins  # get lowest value of cdf (normalized)
        ihigh = np.argmax(cdf >= tol[1]) / nbins  # get hights value of cdf (normalized)

        lut = np.linspace(0, 1, num=nbins)  # create convert map of values
        lut[lut <= ilow] = ilow  # make sure they are larger than lowest value
        lut[lut >= ihigh] = ihigh  # make sure they are smaller than largest value
        lut = (lut - ilow) / (ihigh - ilow)  # normalize between 0 and 1
        lut = np.round(lut * nbins).astype(img.dtype)  # convert to the original image's type

        img_out = np.array([[lut[i] for i in row] for row in img])  # convert input image values based on conversion list

        return img_out

    def randompick(self,n):
        # generate random number from 0 ~ n-1

        return(random.randint(0, n-1))


def main():
    app = QApplication(sys.argv)

    umix = Unmixer()

    sys.exit(app.exec_())



if __name__ == '__main__':
    main()
