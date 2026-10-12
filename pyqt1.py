from PyQt5 import QtWidgets
import sys

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()
window.setWindowTitle("New Program")
window.resize(600, 600)
lible = QtWidgets.QLabel("<center>I Can Do It:)</center>")
btn = QtWidgets.QPushButton("exit")
btn2 = QtWidgets.QPushButton("Ice Cream")
box = QtWidgets.QVBoxLayout()
box.addWidget(lible)
box.addWidget(btn2)
box.addWidget(btn)
window.setLayout(box)
btn.clicked.connect(app.quit)
window.show()
sys.exit(app.exec_())
