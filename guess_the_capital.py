import sys

from PyQt5.QtWidgets import QApplication

from gui.MainWindow import MainWindow


app = QApplication(sys.argv)

w = MainWindow()
w.show()

sys.exit(app.exec_())
