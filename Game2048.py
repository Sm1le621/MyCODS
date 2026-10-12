from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtGui import QPainter, QColor, QFont, QPen
from PyQt5.QtCore import Qt, QRect

import sys, os, copy, random

class GameForm(QMainWindow):
    def __init__(self, parent = None):
        super(GameForm, self).__init__(parent)
        self.initUi()
        #визначити колір фона кожного чила
        self.colors = {0: (204, 192, 179), 2: (238, 228, 218), 
                    4: (237, 224, 200), 8: (242, 177, 121), 
                    16: (245, 149, 99), 32: (246, 124, 95),
                    64: (246, 94, 59), 128: (237, 207, 144),
                    256: (237, 207, 114), 512: (237, 207, 104),
                    1024: (227, 207, 114), 2048: (237, 217, 114),
                    4096: (237, 207, 124), 8192: (237, 227, 120),
                    16384: (220, 207, 114), 32768: (245, 184, 114),
                    65536: (237, 237, 15), 131072: (5, 5, 5),
                    262144: (666, 666, 666), 524288: (199, 707, 777),
                    1048576: (250, 207, 100)
                    }
        self.initGameData()

    def initUi(self):
        #a = random.randint(1, 500)
        self.setWindowTitle("2048")
        self.resize(505, 720)
        self.setFixedSize(self.width(), self.height())
        self.initGameOpt()
    def initGameOpt(self):
        """ініціалізація конфігурації гри"""
        self.lbFont = QFont('Gill Sans MT Condensed', 12)
        self.lgFont = QFont('Gill Sans MT Condensed', 50)
        self.nmFont = QFont('Gill Sans MT Condensed', 36)
    def initGameData(self):
        #ініціалізація ігрового номера
        self.data = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        count = 0
        while count < 2:
            row = random.randint(0, len(self.data)-1)
            col = random.randint(0, len(self.data[0])-1)
            if self.data[row][col] != 0:
                continue
            self.data[row][col] = 2 if random.randint(0, 1) else 4
            count += 1
        self.curScore = 0
        self.bstScore = 0
        if os.path.exists("bestscore.ini"):
            with open("bestscore.ini", "r") as file:
                self.bestScore = int(file.read())

    def PaintEvent(self, e):
        """Переписати подію малювання"""
        qp = QPainter
        qp.begin(self)
        self.darwGameGraph(qp)
        qp.end()
    def drawGameGraph(self, qp):
        self.drawLog(qp)


    def drawLog(self, qp):
        """лого"""
        pen = QPen(QColor(200, 65, 23), 15)
        qp.setFont(self.lgFont)
        qp.setPen(pen)
        qp.drawText(QRect(10, 0, 130, 150), Qt.AlignCenter, "2048")
    def drawLabel(self, qp):
        """інформація на мітках"""
        qp.setFont(self.lbFont)
        qp.setPen(QColor(119, 110, 101))
        qp.drawText(15, 134, "зроби однакові числа і отримай 2048")
        qp.drawText(15, 660, "Як грати:")
        qp.drawText(15, 680, "Використовуємо вліво вправо вверх вниз щоб перемістити квадрат:")
        qp.drawText(45, 700, "з однаковими номерами зустрічаються разом - вони обєднуються в один")



