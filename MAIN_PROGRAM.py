# importing all the modules required
import mysql.connector as sqltor
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication

mydb = sqltor.connect(host="localhost", user="root", passwd="password")# establishing a connection with sql database
sqlcursor = mydb.cursor()# assigning cursor to sqlcursor

class TETS(QDialog):
    def __init__(self):
        super(TETS,self).__init__()
        loadUi("TETS.ui", self)

        self.pushButton_2.clicked.connect(self.toprint)

        sqlcursor.execute("use login")
        sqlcursor.execute("select * from logins")
        data = sqlcursor.fetchall()
        self.tableWidget.setRowCount(len(data))
        tablerow = 0
        for row in data:
            self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
            tablerow += 1

        print((self.tableWidget.item(0,0)).text())

    def toprint(self):
        rowcount = self.tableWidget.rowCount()
        coloumncount = self.tableWidget.coloumnCount()
        for row in range(rowcount):
            rowdata = []
            for colounm in range(coloumncount):
                widgetitem = self.tableWidget.item(row, colounm)
                if(widgetitem and widgetitem.text()):
                    rowdata.append(widgetitem.text())
                else:
                    rowdata.append("NULL")
            print(rowdata)

app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
mainwindow = TETS()
widget.addWidget(mainwindow)
widget.setCurrentIndex(0)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("exiting")
    with open("classdetails.txt", "r") as fh:
        print(fh.read())
