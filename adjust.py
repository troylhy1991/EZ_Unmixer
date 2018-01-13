from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys,os

def main():
	app = QApplication(sys.argv)
	w = Adjust()
	sys.exit(app.exec_())

class Adjust(QWidget):
	def __init__(self, *args):
		QWidget.__init__(self, *args)

		###### Minimum #########
		label1 = QLabel('Minimum')
		self.spinBox1 = QSpinBox()
		self.slider1 = QSlider(Qt.Horizontal)
		HBoxLayout1 = QHBoxLayout()
		HBoxLayout1.addWidget(self.spinBox1)
		HBoxLayout1.addWidget(self.slider1)
		HBoxLayout1.addWidget(label1)

		self.slider1.setRange(0,255)
		self.slider1.setValue(0)
		self.slider1.valueChanged.connect(self.sliderChange1)

		self.spinBox1.setRange(0,255)
		self.spinBox1.setValue(0)
		self.spinBox1.valueChanged.connect(self.spinChange1)

		###### Maximum #####
		label2 = QLabel('Maximum')
		self.spinBox2 = QSpinBox()
		self.slider2 = QSlider(Qt.Horizontal)
		HBoxLayout2 = QHBoxLayout()
		HBoxLayout2.addWidget(self.spinBox2)
		HBoxLayout2.addWidget(self.slider2)
		HBoxLayout2.addWidget(label2)

		self.slider2.setRange(0,255)
		self.slider2.setValue(255)
		self.slider2.valueChanged.connect(self.sliderChange2)

		self.spinBox2.setRange(0,255)
		self.spinBox2.setValue(255)
		self.spinBox2.valueChanged.connect(self.spinChange2)

		##### Brightness #####
		label3 = QLabel('Brightness')
		self.spinBox3 = QSpinBox()
		self.slider3 = QSlider(Qt.Horizontal)
		HBoxLayout3 = QHBoxLayout()
		HBoxLayout3.addWidget(self.spinBox3)
		HBoxLayout3.addWidget(self.slider3)
		HBoxLayout3.addWidget(label3)

		self.slider3.setRange(-10,10)
		self.slider3.setValue(0)
		self.slider3.valueChanged.connect(self.sliderChange3)

		self.spinBox3.setRange(-10,10)
		self.spinBox3.setValue(0)
		self.spinBox3.valueChanged.connect(self.spinChange3)

		##### Contrast ######
		label4 = QLabel('Contrast')
		self.spinBox4 = QSpinBox()
		self.slider4 = QSlider(Qt.Horizontal)
		HBoxLayout4 = QHBoxLayout()
		HBoxLayout4.addWidget(self.spinBox4)
		HBoxLayout4.addWidget(self.slider4)
		HBoxLayout4.addWidget(label4)

		self.slider4.setRange(-10,10)
		self.slider4.setValue(0)
		self.slider4.valueChanged.connect(self.sliderChange4)

		self.spinBox4.setRange(-10,10)
		self.spinBox4.setValue(0)
		self.spinBox4.valueChanged.connect(self.spinChange4)

		self.combo = QComboBox()
		self.combo.addItems(["CH_Master","CH_Leakage"])
		self.Button = QPushButton('reset')
		HBoxLayout5 = QHBoxLayout()
		HBoxLayout5.addWidget(self.combo)
		HBoxLayout5.addWidget(self.Button)

		VBoxLayout = QVBoxLayout()
		VBoxLayout.addLayout(HBoxLayout1)
		VBoxLayout.addLayout(HBoxLayout2)
		VBoxLayout.addLayout(HBoxLayout3)
		VBoxLayout.addLayout(HBoxLayout4)
		VBoxLayout.addLayout(HBoxLayout5)

		self.setLayout(VBoxLayout)
		self.setWindowTitle("Adjust")
		self.setFixedSize(270,400)
		#self.show()

	def spinChange1(self):
		self.slider1.setValue(self.spinBox1.value())
		lower = self.spinBox1.value()
		upper = self.spinBox2.value()
		brightness = self.spinBox3.value()
		contrast = self.spinBox4.value()
		channel = str(self.combo.currentText())
		self.emit(SIGNAL("IMAGEADJUST"), lower, upper, brightness, contrast, channel)


	def spinChange2(self):
		self.slider2.setValue(self.spinBox2.value())

		lower = self.spinBox1.value()
		upper = self.spinBox2.value()
		brightness = self.spinBox3.value()
		contrast = self.spinBox4.value()
		channel = str(self.combo.currentText())
		self.emit(SIGNAL("IMAGEADJUST"), lower, upper, brightness, contrast, channel)

	def spinChange3(self):
		self.slider3.setValue(self.spinBox3.value())

		lower = self.spinBox1.value()
		upper = self.spinBox2.value()
		brightness = self.spinBox3.value()
		contrast = self.spinBox4.value()
		channel = str(self.combo.currentText())
		self.emit(SIGNAL("IMAGEADJUST"), lower, upper, brightness, contrast, channel)

	def spinChange4(self):
		self.slider4.setValue(self.spinBox4.value())

		lower = self.spinBox1.value()
		upper = self.spinBox2.value()
		brightness = self.spinBox3.value()
		contrast = self.spinBox4.value()
		channel = str(self.combo.currentText())
		self.emit(SIGNAL("IMAGEADJUST"), lower, upper, brightness, contrast, channel)

	def sliderChange1(self):
		self.spinBox1.setValue(self.slider1.value())

		lower = self.slider1.value()
		upper = self.slider2.value()
		brightness = self.slider3.value()
		contrast = self.slider4.value()
		channel = str(self.combo.currentText())
		self.emit(SIGNAL("IMAGEADJUST"), lower, upper, brightness, contrast, channel)

	def sliderChange2(self):
		self.spinBox2.setValue(self.slider2.value())

		lower = self.slider1.value()
		upper = self.slider2.value()
		brightness = self.slider3.value()
		contrast = self.slider4.value()
		channel = str(self.combo.currentText())
		self.emit(SIGNAL("IMAGEADJUST"), lower, upper, brightness, contrast, channel)

	def sliderChange3(self):
		self.spinBox3.setValue(self.slider3.value())

		lower = self.slider1.value()
		upper = self.slider2.value()
		brightness = self.slider3.value()
		contrast = self.slider4.value()
		channel = str(self.combo.currentText())
		self.emit(SIGNAL("IMAGEADJUST"), lower, upper, brightness, contrast, channel)

	def sliderChange4(self):
		self.spinBox4.setValue(self.slider4.value())

		lower = self.slider1.value()
		upper = self.slider2.value()
		brightness = self.slider3.value()
		contrast = self.slider4.value()
		channel = str(self.combo.currentText())
		self.emit(SIGNAL("IMAGEADJUST"), lower, upper, brightness, contrast, channel)

if __name__ == "__main__":
    main()
