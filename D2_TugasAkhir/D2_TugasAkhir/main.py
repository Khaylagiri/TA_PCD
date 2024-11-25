import sys
import cv2
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUi
import numpy as np


class ShowImage (QMainWindow):
    def __init__(self):
        super(ShowImage,self).__init__()
        loadUi('GUi.ui',self)
        self.image = None
        self.loadButton.clicked.connect(self.loadClicked)
        self.saveButton.triggered.connect(self.save_Button)
        self.startButton.clicked.connect(self.Cek_Kualitas)

    def Cek_Kualitas(self):
        try:
            # KUALITAS HSV

            img = self.image
            # Crop image
            r = cv2.selectROI(img)
            if r == (0, 0, 0, 0):  # Jika tidak ada ROI yang dipilih
                print("ROI tidak dipilih.")
                return

            images = img[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]

            # Konversi dari BGR ke ruang warna HSV
            hsv = cv2.cvtColor(images, cv2.COLOR_BGR2HSV)

            # Tentukan batas bawah dan atas untuk mask
            lower_blue = np.array([1, 71, 50])
            upper_blue = np.array([40, 215, 255])

            mask = cv2.inRange(hsv, lower_blue, upper_blue)

            result = cv2.bitwise_and(images, images, mask=mask)

            # Hitung mean dari area yang di-mask
            mean = np.mean(result[result > 0])  # Hanya nilai non-zero yang dihitung
            print(mean)

            if 150.1 <= mean <= 200:
                kualitas = 'Kualitas Daging Ke-1 = Daging Sangat Segar'
            elif 100.1 <= mean <= 150:
                kualitas = 'Kualitas Daging Ke-2 = Daging Segar'
            elif 90.1 <= mean <= 100:
                kualitas = 'Kualitas Daging Ke-3 = Daging Biasa'
            elif 80.1 <= mean <= 90:
                kualitas = 'Kualitas Daging Ke-4 = Daging Busuk'
            elif 70 <= mean <= 80:
                kualitas = 'Kualitas Daging Ke-5 = Daging Sangat Busuk'
            else:
                kualitas = 'Kualitas tidak terdeteksi'

            print(kualitas)
            self.label_kualitas_daging.setText(kualitas)
            # self.mean.setText(str(mean))  # Jika ingin menampilkan nilai mean

            self.image = hsv
            self.displayImage(2)

        except Exception as e:
            print(f"Terjadi kesalahan: {e}")

    @pyqtSlot()
    def loadClicked(self):
        flname, filter=QFileDialog.getOpenFileName(self, 'Open File', 'D:\Kuliah\Semester 8\Prak PCD\TugasAkhir\Data_latih',"Image Files(*.jpg; *.jpeg; *.png)")
        if flname:
            self.loadImage(flname)
        else:
            print('Invalid Image')

    def loadImage(self, flname):
        self.image = cv2.imread(flname)
        self.displayImage(1)

    def displayImage(self, windows=1):
        qformat = QImage.Format_Indexed8

        if len(self.image.shape) == 3:
            if (self.image.shape[2]) == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        if windows == 1:
            img = QImage(self.image,
                         self.image.shape[1],
                         self.image.shape[0],
                         self.image.strides[0], qformat)
            img = img.rgbSwapped()
            self.label.setPixmap(QPixmap.fromImage(img))
            self.label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.label.setScaledContents(True)

        elif windows == 2:
            img = QImage(self.image,
                         self.image.shape[1],
                         self.image.shape[0],
                         self.image.strides[0], qformat)
            img = img.rgbSwapped()
            self.label_2.setPixmap(QPixmap.fromImage(img))
            self.label_2.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.label_2.setScaledContents(True)

    def save_Button(self):
        flname, filter = QFileDialog.getSaveFileName(self, 'save file','D:\\',
                                                     "Images Files(*.jpg)")
        if flname:
            cv2.imwrite(flname, self.image)
        else:
            print('Saved')



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ShowImage()
    window.setWindowTitle('Show Image GUI')
    window.show()
    sys.exit(app.exec_())