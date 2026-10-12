import sys, os
from PyQt6 import QtWidgets as QW
from PyQt6 import QtCore as QC

class MainWindow(QW.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        box = QW.QVBoxLayout()

        self.button = QW.QPushButton("GMod")
        self.button2 = QW.QPushButton("TFWR")
        button3 = QW.QPushButton("WallpaperEngine")
        self.button.clicked.connect(self.the_button_was_clicked)
        self.button2.clicked.connect(self.the_button_was_clicked)
        button3.clicked.connect(self.the_button_was_clicked)
        

        self.setFixedSize(QC.QSize(400, 300))
        box.addWidget(self.button)
        box.addWidget(self.button2)
        conteiner = QW.QWidget()
        conteiner.setLayout(box)

        self.setCentralWidget(conteiner)

    def the_button_was_clicked(self):
        print(self.button.clicked.signal.count(""))
        print(self.button2.clicked.signal.count(""))

        """if self.button.clicked.signal.count("ww") == 0:
            os.startfile("steam://rungameid/4000")
            print("GMod Started!")
        elif self.button2.clicked.signal.count("www") == 1:
            os.startfile("steam://rungameid/2060160")
            print("TFWR Started!")"""

app = QW.QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()