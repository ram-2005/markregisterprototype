import mysql.connector as sqltor
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication

class login_pg(QDialog):
    def __init__(self):
        super(login_pg, self).__init__()
        loadUi("project-for-fun.ui", self)# the first page , login page
        self.submit_button.clicked.connect(self.display)
    def display(self):
        self.label_2.setText("FUCK YOU")


app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
mainwindow = login_pg()
widget.addWidget(mainwindow)
widget.setCurrentIndex(0)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("exiting")