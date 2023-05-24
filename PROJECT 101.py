# importing all the modules required
import mysql.connector as sqltor
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtCore import pyqtSlot
#from PyQt5.QtChart import QChart , QPainter , QPen
#from PyQt5.Core import Qt

mydb = sqltor.connect(host="localhost", user="root", passwd="password")# establishing a connection with sql database
sqlcursor = mydb.cursor()# assigning cursor to sqlcursor

class login_pg(QDialog):
    def __init__(self):
        super(login_pg, self).__init__()
        loadUi("pro_login_pg.ui", self)# the first page , login page

        self.submit_button.clicked.connect(self.logingate)

    def logingate(self):
        dbname = ('login',)
        sqlcursor.execute("show databases;")
        data = sqlcursor.fetchall()

        if dbname in data:
           pass

        else:# creating the database if it does not exist
            sqlcursor.execute("create database login")
            sqlcursor.execute("use login")
            sqlcursor.execute("create table logins( username char(130), password char(130), desig char(130))")
            sqlcursor.execute("insert into logins values('masterlogin','12345master67890','master')")
            mydb.commit()

        username = self.username_line.text()
        password = self.password_line.text()
        sqlcursor.execute("use login")
        sqlcursor.execute("select password from logins where username = '"+username+"'")
        data = sqlcursor.fetchall()

        if password == data[0][0]:
            sqlcursor.execute("select desig from logins where username = '"+username+"'")
            item = sqlcursor.fetchall()
            if item[0][0] == "master":
                widget.setCurrentIndex(1)
            if item[0][0] == "staff":
                with open("username.txt", 'w') as fh:
                    fh.write(username)
                widget.setCurrentIndex(4)


        else:
            self.error_label.setText("wrong username or password , please try again....!")

class master_main_pg(QDialog):
    def __init__(self):
        super(master_main_pg,self).__init__()
        loadUi("pro_master_login_main_pg.ui", self)

        self.add_participant_butt.clicked.connect(self.to_addparticipant)
        self.remove_participant_butt.clicked.connect(self.to_removeparticipant)
        self.edit_participant_butt.clicked.connect(self.to_editparticipant)
        self.set_year_butt.clicked.connect(self.to_setyear)

    def to_editparticipant(self):
        widget.setCurrentIndex(17)

    def to_addparticipant(self):
        widget.setCurrentIndex(2)

    def to_removeparticipant(self):
        widget.setCurrentIndex(3)

    def to_setyear(self):
        widget.setCurrentIndex(21)

class add_participant(QDialog):
    def __init__(self):
        super(add_participant, self).__init__()
        loadUi("pro_add_participantant_pg.ui", self)
        self.add_execute.clicked.connect(self.addpart)
        self.prev_pg_execute.clicked.connect(self.prevpage)

    def addpart(self):
        sqlcursor.execute("use login")
        username = self.add_part_username.text()
        desig = self.add_part_desig.text()
        sqlcursor.execute("use login")
        sqlcursor.execute("select username from logins")
        data=sqlcursor.fetchall()
        for item in data:
            if username == item[0]:
                self.message_label.setStyleSheet("color: rgb(255, 0, 0);font: 12pt 'Arial';")
                self.message_label.setText("username already exists")
                break
        else:
            cmd = "insert into logins values('" + username + "', 'password' , '" + desig + "')"
            sqlcursor.execute(cmd)
            mydb.commit()
            self.message_label.setStyleSheet("color: rgb(0,170, 0);font: 12pt 'Arial';")
            self.message_label.setText("participant has been successfully added")

    def prevpage(self):
        widget.setCurrentIndex(1)

class remove_participant(QDialog):
    def __init__(self):
        super(remove_participant,self).__init__()
        loadUi("pro_remove_participant_pg.ui", self)

        self.removepart_remove_execute.clicked.connect(self.remove_part)
        self.removepart_backpg_execute.clicked.connect(self.prevpage)

    def remove_part(self):
        username = self.removeparrt_username.text()
        sqlcursor.execute("use login")
        sqlcursor.execute("select username from logins")
        data = sqlcursor.fetchall()
        for item in data:
            if username == item[0]:
                cmd = "delete from logins where username = '" + username + "'"
                sqlcursor.execute(cmd)
                mydb.commit()
                self.message_label.setStyleSheet("color: rgb(0,170,0);font: 12pt 'Arial';")
                self.message_label.setText("the participant has been removed")
                break
        else:
            self.message_label.setStyleSheet("color: rgb(255, 0, 0);font: 12pt 'Arial';")
            self.message_label.setText("the given username doesn't exit")

    def prevpage(self):
        widget.setCurrentIndex(1)


class staff_login_main_pg(QDialog):
    def __init__(self):
        super(staff_login_main_pg,self).__init__()
        loadUi("pro_teacherlogin_main_pg.ui", self)

        with open("username.txt",'r') as  fh:
            username = fh.read().strip().title()
        self.teacherlogin_username.setText(username)
        with open("notice.txt", 'r') as fh:
            data = fh.read()
            self.teacherlogin_notice.setText(data)

        self.addsett.clicked.connect(self.to_additinol_sett)
        self.taecherlogin_addmarks.clicked.connect(self.to_addmarks)
        self.taecherlogin_editmarks.clicked.connect(self.to_editmarks)
        self.taecherlogin_classprogress.clicked.connect(self.to_classprogress)
        self.taecherlogin_studentprogress.clicked.connect(self.to_stuprogress)
        self.taecherlogin_archives.clicked.connect(self.to_archives)



    def to_additinol_sett(self):
        widget.setCurrentIndex(13)
    def to_addmarks(self):
        widget.setCurrentIndex(5)
    def to_editmarks(self):
        widget.setCurrentIndex(28)
    def to_classprogress(self):
        widget.setCurrentIndex(41)
    def to_stuprogress(self):
        pass
    def to_archives(self):
        pass


class addmarks_selectclass(QDialog):
    def __init__(self):
        super(addmarks_selectclass, self).__init__()
        loadUi("pro_addmarks_main_pg.ui", self)

        self.back.clicked.connect(self.to_prevpg)
        self.teacherlogin_class_1.clicked.connect(self.setclass1)
        self.teacherlogin_class_2.clicked.connect(self.setclass2)
        self.teacherlogin_class_3.clicked.connect(self.setclass3)
        self.teacherlogin_class_4.clicked.connect(self.setclass4)
        self.teacherlogin_class_5.clicked.connect(self.setclass5)
        self.teacherlogin_class_6.clicked.connect(self.setclass6)
        self.teacherlogin_class_7.clicked.connect(self.setclass7)
        self.teacherlogin_class_8.clicked.connect(self.setclass8)
        self.teacherlogin_class_9.clicked.connect(self.setclass9)
        self.teacherlogin_class_10.clicked.connect(self.setclass10)
        self.teacherlogin_class_11.clicked.connect(self.setclass11)
        self.teacherlogin_class_12.clicked.connect(self.setclass12)

    def setclass1(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class1\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(6)

    def setclass2(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class2\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(6)

    def setclass3(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class3\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(8)

    def setclass4(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class4\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(8)

    def setclass5(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class5\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(8)

    def setclass6(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class6\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(8)

    def setclass7(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class7\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(8)

    def setclass8(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class8\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(8)

    def setclass9(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class9\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(8)

    def setclass10(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class10\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(8)

    def setclass11(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class11\n", "subject\n", "test\n","stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(9)

    def setclass12(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class12\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(9)

    def to_prevpg(self):
        widget.setCurrentIndex(4)

class addmarks_selectsubject_12(QDialog):
    def __init__(self):
        super(addmarks_selectsubject_12,self).__init__()
        loadUi("pro_addmarks_subject_class12_pg.ui", self)

        self.back_execute.clicked.connect(self.to_prevpg)
        self.teacherlogin_subject_english.clicked.connect(self.seteng)
        self.teacherlogin_subject_evs.clicked.connect(self.setevs)
        self.teacherlogin_subject_maths.clicked.connect(self.setmat)
        self.teacherlogin_subject_lang2.clicked.connect(self.setlan)
        self.teacherlogin_subject_comp.clicked.connect(self.setcom)

    def seteng(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "english\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(7)

    def setevs(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "evs\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(7)

    def setmat(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "maths\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(7)

    def setlan(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "lang2\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(7)

    def setcom(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "computer\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(7)

    def to_prevpg(self):
        widget.setCurrentIndex(5)

class addmarks_selectsubject_345678910(QDialog):
    def __init__(self):
        super(addmarks_selectsubject_345678910, self).__init__()
        loadUi("pro_addmarks_subject_class345678910_pg.ui", self)

        self.back_execute.clicked.connect(self.to_prevpg)
        self.teacherlogin_subject_english.clicked.connect(self.seteng)
        self.teacherlogin_subject_science.clicked.connect(self.setsci)
        self.teacherlogin_subject_maths.clicked.connect(self.setmat)
        self.teacherlogin_subject_lang2.clicked.connect(self.setlan)
        self.teacherlogin_subject_comp.clicked.connect(self.setcom)
        self.teacherlogin_subject_social.clicked.connect(self.setsoc)

    def seteng(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "english\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class10\n":
            widget.setCurrentIndex(16)
        else:
            widget.setCurrentIndex(7)

    def setsci(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "science\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class10\n":
            widget.setCurrentIndex(16)
        else:
            widget.setCurrentIndex(7)

    def setmat(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "maths\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class10\n":
            widget.setCurrentIndex(16)
        else:
            widget.setCurrentIndex(7)


    def setlan(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "lang2\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class10\n":
            widget.setCurrentIndex(16)
        else:
            widget.setCurrentIndex(7)

    def setcom(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "computer\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class10\n":
            widget.setCurrentIndex(16)
        else:
            widget.setCurrentIndex(7)

    def setsoc(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "social\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class10\n":
            widget.setCurrentIndex(16)
        else:
            widget.setCurrentIndex(7)

    def to_prevpg(self):
        widget.setCurrentIndex(5)

class addmarks_select_stream(QDialog):
    def __init__(self):
        super(addmarks_select_stream, self).__init__()
        loadUi("pro_addmarks_stream_pg.ui", self)

        self.back_execute.clicked.connect(self.to_prevpg)
        self.addmarks_stream_biomaths.clicked.connect(self.setbiomaths)
        self.addmarks_stream_computer.clicked.connect(self.setcomputersci)
        self.addmarks_stream_commerce.clicked.connect(self.setcommerce)

    def setbiomaths(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[3] = "biomaths\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(10)

    def setcomputersci(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[3] = "computermath\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(11)

    def setcommerce(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[3] = "commerce\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(12)

    def to_prevpg(self):
        widget.setCurrentIndex(5)

class select_test_typ1_pg(QDialog):
    def __init__(self):
        super(select_test_typ1_pg,self).__init__()
        loadUi("pro_addmarks_exam_type1_pg.ui", self)

        self.back_execute.clicked.connect(self.to_prevpg)
        self.teacherlogin_exam_pt1.clicked.connect(self.setpt1)
        self.teacherlogin_exam_pt2.clicked.connect(self.setpt2)
        self.teacherlogin_exam_pt3.clicked.connect(self.setpt3)
        self.teacherlogin_exam_pt4.clicked.connect(self.setpt4)
        self.teacherlogin_subjeteacherlogin_exam_halfyear.clicked.connect(self.sethalfyear)
        self.teacherlogin_exam_annual.clicked.connect(self.setannual)

    def setpt1(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[2] = "periodictest1\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(24)

    def setpt2(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[2] = "periodictest2\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(24)

    def setpt3(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[2] = "periodictest3\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(24)

    def setpt4(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[2] = "periodictest4\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(24)

    def sethalfyear(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[2] = "halfyearly\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(24)

    def setannual(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[2] = "annual\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(24)

    def to_prevpg(self):
        with open("classdetails.txt", "r") as fh:
            cls=fh.readlines()
        if cls[0] in ("class11\n","class12\n"):
            if cls[3] == "biomaths\n":
                widget.setCurrentIndex(10)
            if cls[3] == "computermath\n":
                widget.setCurrentIndex(11)
            if cls[3] == "commerce\n":
                widget.setCurrentIndex(12)
        elif cls[0][-2] in ("3","4","5","6","7","8","9","0",) and cls[0][-3] in ("s","1",):
            widget.setCurrentIndex(8)
        elif cls[0][-2] in ("1","2") and cls[0][-3] in ("s"):
            widget.setCurrentIndex(6)



class select_subject_biomaths_pg(QDialog):
    def __init__(self):
        super(select_subject_biomaths_pg,self).__init__()
        loadUi("pro_addmarks_subject_class1211_biomaths_pg.ui", self)

        self.back_execute.clicked.connect(self.to_prevpg)
        self.teacherlogin_subject_english.clicked.connect(self.seteng)
        self.teacherlogin_subject_biology.clicked.connect(self.setbio)
        self.teacherlogin_subject_maths.clicked.connect(self.setmat)
        self.teacherlogin_subject_chemistry.clicked.connect(self.setche)
        self.teacherlogin_subject_physcis.clicked.connect(self.setphy)

    def seteng(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "english\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class12\n":
            widget.setCurrentIndex(16)
        else:
            widget.setCurrentIndex(7)

    def setbio(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "biology\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class12\n":
            widget.setCurrentIndex(16)
        else:
            widget.setCurrentIndex(7)

    def setmat(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "maths\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class12\n":
            widget.setCurrentIndex(16)
        else:
            widget.setCurrentIndex(7)


    def setche(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "chemistry\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class12\n":
            widget.setCurrentIndex(16)
        else:
            widget.setCurrentIndex(7)

    def setphy(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "physics\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class12\n":
            widget.setCurrentIndex(16)
        else:
            widget.setCurrentIndex(7)

    def to_prevpg(self):
        widget.setCurrentIndex(9)

class select_subject_computersci_pg(QDialog):
    def __init__(self):
        super(select_subject_computersci_pg,self).__init__()
        loadUi("pro_addmarks_subject_class1211_compmaths_pg.ui", self)

        self.back_execute.clicked.connect(self.to_prevpg)
        self.teacherlogin_subject_english.clicked.connect(self.seteng)
        self.teacherlogin_subject_computer.clicked.connect(self.setcomp)
        self.teacherlogin_subject_maths.clicked.connect(self.setmat)
        self.teacherlogin_subject_chemistry.clicked.connect(self.setche)
        self.teacherlogin_subject_physcis.clicked.connect(self.setphy)

    def seteng(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "english\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class12\n":
            widget.setCurrentIndex(16)
        else:
            widget.setCurrentIndex(7)


    def setcomp(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "computer\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class12\n":
            widget.setCurrentIndex(16)
        else:
            widget.setCurrentIndex(7)

    def setmat(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "maths\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class12\n":
            widget.setCurrentIndex(16)
        else:
            widget.setCurrentIndex(7)


    def setche(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "chemistry\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class12\n":
            widget.setCurrentIndex(16)
        else:
            widget.setCurrentIndex(7)


    def setphy(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "physics\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class12\n":
            widget.setCurrentIndex(16)
        else:
            widget.setCurrentIndex(7)


    def to_prevpg(self):
        widget.setCurrentIndex(9)

class select_subject_commerce_pg(QDialog):
    def __init__(self):
        super(select_subject_commerce_pg, self).__init__()
        loadUi("pro_addmarks_subject_class1211_commerce_pg.ui", self)

        self.back_execute.clicked.connect(self.to_prevpg)
        self.teacherlogin_subject_english.clicked.connect(self.seteng)
        self.teacherlogin_subject_computer.clicked.connect(self.setcomp)
        self.teacherlogin_subject_buisness.clicked.connect(self.setbuss)
        self.teacherlogin_subject_accounts.clicked.connect(self.setacc)
        self.teacherlogin_subject_economics.clicked.connect(self.seteco)

    def seteng(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "english\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class12\n":
            widget.setCurrentIndex(16)
        else:
            widget.setCurrentIndex(7)


    def setcomp(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "computer\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class12\n":
            widget.setCurrentIndex(16)
        else:
            widget.setCurrentIndex(7)

    def setbuss(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "business\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class12\n":
            widget.setCurrentIndex(16)
        else:
            widget.setCurrentIndex(7)

    def setacc(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "accounts\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class12\n":
            widget.setCurrentIndex(16)
        else:
            widget.setCurrentIndex(7)


    def seteco(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "economics\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class12\n":
            widget.setCurrentIndex(16)
        else:
            widget.setCurrentIndex(7)

    def to_prevpg(self):
        widget.setCurrentIndex(9)

class additional_settings_pg(QDialog):
    def __init__(self):
        super(additional_settings_pg,self).__init__()
        loadUi("additional_settings_pg.ui", self)

        self.back.clicked.connect(self.to_prevpg)
        self.change_password.clicked.connect(self.to_chg_pass)
        self.set_notice.clicked.connect(self.to_set_notice)
        #self.creator_info.clicked.connect(self.to_creator_info)

    def to_chg_pass(self):
        widget.setCurrentIndex(14)

    def to_prevpg(self):
        widget.setCurrentIndex(4)

    def to_set_notice(self):
        widget.setCurrentIndex(15)



class change_password_pg(QDialog):
    def __init__(self):
        super(change_password_pg,self).__init__()
        loadUi("change_password_pg.ui", self)

        self.change_password.clicked.connect(self.changepass)
        self.back.clicked.connect(self.to_prevpg)

    def changepass(self):
        newpassword=self.password_line.text()
        with open("username.txt",'r') as fh :
            username = fh.read().strip()
        cmd = "update logins set password = '"+ newpassword +"' where username = '"+username+"'"
        sqlcursor.execute("use login")
        sqlcursor.execute(cmd)
        mydb.commit()
        self.message_label.setText("Password has been successfully changed")

    def to_prevpg(self):
        widget.setCurrentIndex(13)

class set_notice(QDialog):
    def __init__(self):
        super(set_notice,self).__init__()
        loadUi("set_notice_pg.ui", self)

        self.change.clicked.connect(self.change_notice)
        self.back.clicked.connect(self.to_prevpg)

    def change_notice(self):
        with open("username.txt",'r') as fh:
            username=fh.read().strip()
        new_notice = self.new_notice.toPlainText()+"\n -"+username
        with open("notice.txt",'w') as fh:
            fh.write(new_notice)
        self.message_label_2.setText("notice changed successfully")

    def to_prevpg(self):
        widget.setCurrentIndex(13)

class select_test_type2(QDialog):
    def __init__(self):
        super(select_test_type2,self).__init__()
        loadUi("pro_addmarks_exam_type2_pg.ui", self)

        self.back_execute.clicked.connect(self.to_prevpg)
        self.teacherlogin_exam_monthly.clicked.connect(self.to_month)
        self.teacherlogin_exam_unit.clicked.connect(self.to_uni)
        self.teacherlogin_exam_preboard.clicked.connect(self.to_pre)

    def to_month(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[2] = "monthly\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(25)

    def to_uni(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[2] = "unit\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(26)

    def to_pre(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[2] = "pre\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(27)

    def to_prevpg(self):
        with open("classdetails.txt", "r") as fh:
            cls = fh.readlines()
        if cls[0] in ("class11\n", "class12\n"):
            if cls[3] == "biomaths\n":
                widget.setCurrentIndex(10)
            if cls[3] == "computermath\n":
                widget.setCurrentIndex(11)
            if cls[3] == "commerce\n":
                widget.setCurrentIndex(12)
        elif cls[0][-2] in ("3", "4", "5", "6", "7", "8", "9", "0",) and cls[0][-3] in ("s", "1",):
            widget.setCurrentIndex(8)
        elif cls[0][-2] in ("1", "2") and cls[0][-3] in ("s"):
            widget.setCurrentIndex(6)

class edit_participant(QDialog):
    def __init__(self):
        super(edit_participant,self).__init__()
        loadUi("pro_editpart_main_pg.ui", self)

        self.back.clicked.connect(self.to_prevpg)
        self.editpart_class_1.clicked.connect(self.setclass1)
        self.editpart_class_2.clicked.connect(self.setclass2)
        self.editpart_class_3.clicked.connect(self.setclass3)
        self.editpart_class_4.clicked.connect(self.setclass4)
        self.editpart_class_5.clicked.connect(self.setclass5)
        self.editpart_class_6.clicked.connect(self.setclass6)
        self.editpart_class_7.clicked.connect(self.setclass7)
        self.editpart_class_8.clicked.connect(self.setclass8)
        self.editpart_class_9.clicked.connect(self.setclass9)
        self.editpart_class_10.clicked.connect(self.setclass10)
        self.editpart_class_11.clicked.connect(self.setclass11)
        self.editpart_class_12.clicked.connect(self.setclass12)

    def setclass1(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class1\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(19)

    def setclass2(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class2\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(19)

    def setclass3(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class3\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(19)

    def setclass4(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class4\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(19)

    def setclass5(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class5\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(19)

    def setclass6(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class6\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(19)

    def setclass7(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class7\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(19)

    def setclass8(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class8\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(19)

    def setclass9(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class9\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(19)

    def setclass10(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class10\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(19)

    def setclass11(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class11\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(18)

    def setclass12(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class12\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(18)

    def to_prevpg(self):
        widget.setCurrentIndex(1)

class edit_participant_select_stream(QDialog):
    def __init__(self):
        super(edit_participant_select_stream,self).__init__()
        loadUi("pro_editpart_select_stream_pg.ui", self)

        self.back_execute.clicked.connect(self.to_prevpg)
        self.addmarks_stream_biomaths.clicked.connect(self.setbiomaths)
        self.addmarks_stream_computer.clicked.connect(self.setcomputersci)
        self.addmarks_stream_commerce.clicked.connect(self.setcommerce)

    def setbiomaths(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[3] = "biomaths\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(19)

    def setcomputersci(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[3] = "computermath\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(19)

    def setcommerce(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[3] = "commerce\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(19)

    def to_prevpg(self):
        widget.setCurrentIndex(17)

class edit_participant_select_table(QDialog):
    def __init__(self):
        super(edit_participant_select_table,self).__init__()
        loadUi("pro_editpart_select_table_pg.ui", self)

        self.back.clicked.connect(self.to_prevpg)
        self.editpart_table_teacher.clicked.connect(self.to_teachertable)
        self.editpart_table_student.clicked.connect(self.to_studenttable)

    def to_teachertable(self):
        widget.setCurrentIndex(20)

    def to_studenttable(self):
        widget.setCurrentIndex(22)

    def to_prevpg(self):
        with open("classdetails.txt", "r") as fh:
            cls = fh.readlines()
        if cls[0] in ("class11\n", "class12\n"):
            widget.setCurrentIndex(18)
        elif cls[0][-2] in ("3", "4", "5", "6", "7", "8", "9", "0",) and cls[0][-3] in ("s", "1",):
            widget.setCurrentIndex(17)
        elif cls[0][-2] in ("1", "2") and cls[0][-3] in ("s"):
            widget.setCurrentIndex(17)

class edit_participant_teacher_table(QDialog):
    def __init__(self):
        super(edit_participant_teacher_table,self).__init__()
        loadUi("pro_editpart_teacher_table_pg.ui", self)

        self.back.clicked.connect(self.to_prevpg)
        self.refresh1.clicked.connect(self.refresh)
        self.submit.clicked.connect(self.add_to_db)

    def add_to_db(self):
        rw1 = []
        rw2 = []
        rwcount = self.tableWidget.rowCount()
        for rw_no in range(rwcount):
            rw_item = self.tableWidget.item(rw_no, 0).text()
            clm_item = self.tableWidget.item(rw_no, 1).text()
            rw1.append(rw_item)
            rw2.append(clm_item)

        with open("currentyear.txt",'r') as fh:
            curntyear = fh.read().strip()
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        if clsdetails[0] =="class1\n":
            tablename = curntyear +"_class1_teacher_table"
        if clsdetails[0] =="class2\n":
            tablename = curntyear +"_class2_teacher_table"
        if clsdetails[0] =="class3\n":
            tablename = curntyear +"_class3_teacher_table"
        if clsdetails[0] =="class4\n":
            tablename = curntyear +"_class4_teacher_table"
        if clsdetails[0] =="class5\n":
            tablename = curntyear +"_class5_teacher_table"
        if clsdetails[0] =="class6\n":
            tablename = curntyear +"_class6_teacher_table"
        if clsdetails[0] =="class7\n":
            tablename = curntyear +"_class7_teacher_table"
        if clsdetails[0] =="class8\n":
            tablename = curntyear + "_class8_teacher_table"
        if clsdetails[0] =="class9\n":
            tablename = curntyear +"_class9_teacher_table"
        if clsdetails[0] =="class10\n":
            tablename = curntyear + "_class10_teacher_table"
        if clsdetails[0] =="class11\n":
            if clsdetails[3] == "biomaths\n":
                tablename = curntyear + "_class11_biomaths_teacher_table"
            elif clsdetails[3] == "computermath\n":
                tablename = curntyear + "_class11_teacher_compmaths_table"
            elif clsdetails[3] == "commerce\n":
                tablename = curntyear + "_class11_teacher_commerce_table"
        if clsdetails[0] =="class12\n":
            if clsdetails[3] == "biomaths\n":
                tablename = curntyear + "_class12_biomaths_teacher_table"
            elif clsdetails[3] == "computermath\n":
                tablename = curntyear + "_class12_teacher_compmaths_table"
            elif clsdetails[3] == "commerce\n":
                tablename = curntyear + "_class12_teacher_commerce_table"

        cmd = "use "+curntyear
        sqlcursor.execute(cmd)
        sqlcursor.execute("show tables")
        qury = sqlcursor.fetchall()
        for item in qury:
            if item[0] == tablename:
                cmd = "delete from " + tablename
                sqlcursor.execute(cmd)
                mydb.commit()
                break
        else:
            cmd = "create table "+tablename+"( role varchar(50) , username varchar(50))"
            sqlcursor.execute(cmd)

        for i in range(len(rw1)):
            cmd = "insert into " + tablename + "(role, username) values('{}','{}')".format(rw1[i], rw2[i])
            sqlcursor.execute(cmd)
        mydb.commit()
        self.message_label.setStyleSheet("color: rgb(0,170, 0);font: 12pt 'Arial';")
        self.message_label.setText("The table has been saved")


    def refresh(self):
        with open("classdetails.txt", "r") as fh:
            cls = fh.readlines()
        if cls[0] in ("class11\n", "class12\n"):
            if cls[3] == "biomaths\n":
                clsinfo = ["class teacher", "english", "biology", "physics", "chemistry", "maths"]
            elif cls[3] == "computermath\n":
                clsinfo = ["class teacher", "english", "computer", "physics", "chemistry", "maths"]
            elif cls[3] == "commerce\n":
                clsinfo = ["class teacher", "english", "computer", "accounts", "buissness", "economics"]
        elif cls[0][-2] in ("3", "4", "5", "6", "7", "8", "9", "0",) and cls[0][-3] in ("s", "1",) and cls[3] == "stream\n":
            clsinfo = ["class teacher", "english", "social", "science", "maths", "tamil", "hindi", "computer"]
        elif cls[0][-2] in ("1", "2") and cls[0][-3] in ("s") and cls[3] == "stream\n":
            clsinfo = ["class teacher", "english", "evs", "maths", "tamil", "hindi", "computer"]

        self.tableWidget.setRowCount(len(clsinfo))
        rowcount = 0
        for item in clsinfo:
            self.tableWidget.setItem(rowcount, 0, QtWidgets.QTableWidgetItem(item))
            rowcount += 1

    def to_prevpg(self):
        widget.setCurrentIndex(19)

class pro_set_year_pg(QDialog):
    def __init__(self):
        super(pro_set_year_pg,self).__init__()
        loadUi("pro_set_year_pg.ui", self)

        self.setyear_execute.clicked.connect(self.ex_setyear)
        self.setyear_backpg_execute.clicked.connect(self.to_prevpg)

    def ex_setyear(self):
        year = self.setyear_year.text()
        curntyear = "year"+year
        sqlcursor.execute("show databases")
        qury = sqlcursor.fetchall()
        for item in qury:
            if item[0] == curntyear:
                with open("currentyear.txt", 'w') as fh:
                    inf = "year" + year
                    fh.write(inf)
                self.message_label.setStyleSheet("color: rgb(0,170, 0);font: 12pt 'Arial';")
                self.message_label.setText("The Current year has been changed")
                break
        else:
            cmd = "create database year" + year
            sqlcursor.execute(cmd)
            mydb.commit()
            with open("currentyear.txt", 'w') as fh:
                inf = "year" + year
                fh.write(inf)
            self.message_label.setStyleSheet("color: rgb(0,170, 0);font: 12pt 'Arial';")
            self.message_label.setText("The Current year has been changed")

    def to_prevpg(self):
        widget.setCurrentIndex(1)

class pro_editpart_student_no_pg(QDialog):
    def __init__(self):
        super(pro_editpart_student_no_pg,self).__init__()
        loadUi("pro_editpart_no_of_student_pg.ui", self)

        self.enter_exe.clicked.connect(self.getvalues)
        self.back.clicked.connect(self.to_prevpg)

    def getvalues(self):
        no_students = self.no_of_students.text()
        with open("no_of_students.txt",'w') as fh:
            fh.write(no_students)
        widget.setCurrentIndex(23)

    def to_prevpg(self):
        widget.setCurrentIndex(19)

class pro_editpart_student_table_pg(QDialog):
    def __init__(self):
        super(pro_editpart_student_table_pg,self).__init__()
        loadUi("pro_editpart_student_table_pg.ui", self)

        self.back.clicked.connect(self.to_prevpg)
        self.refresh.clicked.connect(self.to_refresh)
        self.submit.clicked.connect(self.add_to_db)

    def add_to_db(self):
        rw1 = []
        rw2 = []
        rwcount = self.tableWidget.rowCount()
        for rw_no in range(rwcount):
            rw_item = self.tableWidget.item(rw_no, 0).text()
            clm_item = self.tableWidget.item(rw_no, 1).text()
            rw1.append(rw_item)
            rw2.append(clm_item)

        with open("currentyear.txt", 'r') as fh:
            curntyear = fh.read().strip()
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        if clsdetails[0] == "class1\n":
            tablename = curntyear + "_class1_student_table"
        if clsdetails[0] == "class2\n":
            tablename = curntyear + "_class2_student_table"
        if clsdetails[0] == "class3\n":
            tablename = curntyear + "_class3_student_table"
        if clsdetails[0] == "class4\n":
            tablename = curntyear + "_class4_student_table"
        if clsdetails[0] == "class5\n":
            tablename = curntyear + "_class5_student_table"
        if clsdetails[0] == "class6\n":
            tablename = curntyear + "_class6_student_table"
        if clsdetails[0] == "class7\n":
            tablename = curntyear + "_class7_student_table"
        if clsdetails[0] == "class8\n":
            tablename = curntyear + "_class8_student_table"
        if clsdetails[0] == "class9\n":
            tablename = curntyear + "_class9_student_table"
        if clsdetails[0] == "class10\n":
            tablename = curntyear + "_class10_student_table"
        if clsdetails[0] == "class11\n":
            if clsdetails[3] == "biomaths\n":
                tablename = curntyear + "_class11_biomaths_student_table"
            elif clsdetails[3] == "computermath\n":
                tablename = curntyear + "_class11_compmaths_student_table"
            elif clsdetails[3] == "commerce\n":
                tablename = curntyear + "_class11_commerce_student_table"
        if clsdetails[0] == "class12\n":
            if clsdetails[3] == "biomaths\n":
                tablename = curntyear + "_class12_biomaths_student_table"
            elif clsdetails[3] == "computermath\n":
                tablename = curntyear + "_class12_compmaths_student_table"
            elif clsdetails[3] == "commerce\n":
                tablename = curntyear + "_class12_commerce_student_table"

        cmd = "use " + curntyear
        sqlcursor.execute(cmd)
        sqlcursor.execute("show tables")
        qury = sqlcursor.fetchall()
        for item in qury:
            if item[0] == tablename:
                cmd = "delete from " + tablename
                sqlcursor.execute(cmd)
                mydb.commit()
                break
        else:
            cmd = "create table " + tablename + "( rollno varchar(50) , username varchar(50))"
            sqlcursor.execute(cmd)

        for i in range(len(rw1)):
            cmd = "insert into " + tablename + "( rollno , username) values('{}','{}')".format(rw1[i], rw2[i])
            sqlcursor.execute(cmd)
        mydb.commit()
        self.message_label.setStyleSheet("color: rgb(0,170, 0);font: 12pt 'Arial';")
        self.message_label.setText("The table has been saved")

    def to_refresh(self):
        with open("no_of_students.txt", "r") as fh:
            no_stu = int(fh.read().strip())

        self.tableWidget.setRowCount(no_stu)
        rowcount = 0
        for i in range(1,(no_stu+1)):
            with open("classdetails.txt", 'r') as fh:
                clsdetails = fh.readlines()
            if clsdetails[0] == "class1\n":
                self.tableWidget.setItem(rowcount, 0, QtWidgets.QTableWidgetItem(str(100+i)))
                rowcount += 1
            if clsdetails[0] == "class2\n":
                self.tableWidget.setItem(rowcount, 0, QtWidgets.QTableWidgetItem(str(200+i)))
                rowcount += 1
            if clsdetails[0] == "class3\n":
                self.tableWidget.setItem(rowcount, 0, QtWidgets.QTableWidgetItem(str(300+i)))
                rowcount += 1
            if clsdetails[0] == "class4\n":
                self.tableWidget.setItem(rowcount, 0, QtWidgets.QTableWidgetItem(str(400+i)))
                rowcount += 1
            if clsdetails[0] == "class5\n":
                self.tableWidget.setItem(rowcount, 0, QtWidgets.QTableWidgetItem(str(500+i)))
                rowcount += 1
            if clsdetails[0] == "class6\n":
                self.tableWidget.setItem(rowcount, 0, QtWidgets.QTableWidgetItem(str(600+i)))
                rowcount += 1
            if clsdetails[0] == "class7\n":
                self.tableWidget.setItem(rowcount, 0, QtWidgets.QTableWidgetItem(str(700+i)))
                rowcount += 1
            if clsdetails[0] == "class8\n":
                self.tableWidget.setItem(rowcount, 0, QtWidgets.QTableWidgetItem(str(800+i)))
                rowcount += 1
            if clsdetails[0] == "class9\n":
                self.tableWidget.setItem(rowcount, 0, QtWidgets.QTableWidgetItem(str(900+i)))
                rowcount += 1
            if clsdetails[0] == "class10\n":
                self.tableWidget.setItem(rowcount, 0, QtWidgets.QTableWidgetItem(str(1000+i)))
                rowcount += 1
            if clsdetails[0] == "class11\n":
                if clsdetails[3] == "biomaths\n":
                    self.tableWidget.setItem(rowcount, 0, QtWidgets.QTableWidgetItem(str(1100+i)+"bm"))
                    rowcount += 1
                elif clsdetails[3] == "computermath\n":
                    self.tableWidget.setItem(rowcount, 0, QtWidgets.QTableWidgetItem(str(1100+i)+"cm"))
                    rowcount += 1
                elif clsdetails[3] == "commerce\n":
                    self.tableWidget.setItem(rowcount, 0, QtWidgets.QTableWidgetItem(str(1100+i)+"cc"))
                    rowcount += 1
            if clsdetails[0] == "class12\n":
                if clsdetails[3] == "biomaths\n":
                    self.tableWidget.setItem(rowcount, 0, QtWidgets.QTableWidgetItem(str(1200+i)+"bm"))
                    rowcount += 1
                elif clsdetails[3] == "computermath\n":
                    self.tableWidget.setItem(rowcount, 0, QtWidgets.QTableWidgetItem(str(1200+i)+"cm"))
                    rowcount += 1
                elif clsdetails[3] == "commerce\n":
                    self.tableWidget.setItem(rowcount, 0, QtWidgets.QTableWidgetItem(str(1200+i)+"cc"))
                    rowcount += 1

    def to_prevpg(self):
        widget.setCurrentIndex(19)

class pro_addmarks_student_table_pg(QDialog):
    def __init__(self):
        super(pro_addmarks_student_table_pg,self).__init__()
        loadUi("pro_addmarks_student_table_pg.ui", self)

        self.back.clicked.connect(self.to_prevpg)
        self.refresh.clicked.connect(self.to_refresh)
        self.submit.clicked.connect(self.add_to_db)

    def add_to_db(self):
        rw1 = []
        rw2 = []
        rw3 = []
        rwcount = self.tableWidget.rowCount()
        for rw_no in range(rwcount):
            rw_item = self.tableWidget.item(rw_no, 0).text()
            rw2_item = self.tableWidget.item(rw_no, 1).text()
            rw3_item = self.tableWidget.item(rw_no, 2).text()
            rw1.append(rw_item)
            rw2.append(rw2_item)
            rw3.append(rw3_item)
        with open("currentyear.txt", 'r') as fh:
            curntyear = fh.read().strip()

        dat_typ_1 = {"english\n": "english", "evs\n": "evs", "maths\n": "maths", "lang2\n": "lang2","computer\n": "computer"}
        dat_typ_2 = {"english\n": "english","science\n": "science","social\n": "social","lang2\n": "language","maths\n": "maths", "computer\n": "computer"}
        dat_typ_3 = {"english\n": "english","biology\n": "biology","physics\n": "physics","chemistry\n": "chemistry", "maths\n": "maths"}
        dat_typ_4 = {"english\n": "english","computer\n": "computer","accounts\n": "accounts","economics\n":"economics", "business\n": "business"}
        dat_typ_5 = {"english\n": "english","computer\n": "computer","physics\n": "physics","chemistry\n":"chemistry", "maths\n": "maths"}

        test_typ1 = {"periodictest1\n": "periodic_test_1", "periodictest2\n": "periodic_test_2", "periodictest3\n":"periodic_test_3", "periodictest4\n":"periodic_test_4", "halfyearly\n":"halfyearly", "annual\n":"annual"}
        test_typ2 = {"monthly\n":"monthly","unit\n":"unit","pre\n":"pre"}


        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        if clsdetails[0] == "class1\n":
            tablename = curntyear + "_class1_"
        if clsdetails[0] == "class2\n":
            tablename = curntyear + "_class2_"
        if clsdetails[0] == "class3\n":
            tablename = curntyear + "_class3_"
        if clsdetails[0] == "class4\n":
            tablename = curntyear + "_class4_"
        if clsdetails[0] == "class5\n":
            tablename = curntyear + "_class5_"
        if clsdetails[0] == "class6\n":
            tablename = curntyear + "_class6_"
        if clsdetails[0] == "class7\n":
            tablename = curntyear + "_class7_"
        if clsdetails[0] == "class8\n":
            tablename = curntyear + "_class8_"
        if clsdetails[0] == "class9\n":
            tablename = curntyear + "_class9_"
        if clsdetails[0] == "class10\n":
            tablename = curntyear + "_class10_"
        if clsdetails[0] == "class11\n":
            if clsdetails[3] == "biomaths\n":
                tablename = curntyear + "_class11_biomaths_"
            elif clsdetails[3] == "computermath\n":
                tablename = curntyear + "_class11_compmaths_"
            elif clsdetails[3] == "commerce\n":
                tablename = curntyear + "_class11_commerce_"
        if clsdetails[0] == "class12\n":
            if clsdetails[3] == "biomaths\n":
                tablename = curntyear + "_class12_biomaths_"
            elif clsdetails[3] == "computermath\n":
                tablename = curntyear + "_class12_compmaths_"
            elif clsdetails[3] == "commerce\n":
                tablename = curntyear + "_class12_commerce_"

        if clsdetails[0] in ("class12\n"):
            if clsdetails[3] == "biomaths\n":
                tablename = tablename + dat_typ_3[clsdetails[1]]+"_"+ test_typ2[clsdetails[2]]
            elif clsdetails[3] == "computermath\n":
                tablename = tablename +dat_typ_4[clsdetails[1]]+"_"+test_typ2[clsdetails[2]]
            elif clsdetails[3] == "commerce\n":
                tablename = tablename +dat_typ_5[clsdetails[1]]+"_"+test_typ2[clsdetails[2]]
        if clsdetails[0] in ("class11\n"):
            if clsdetails[3] == "biomaths\n":
                tablename = tablename +dat_typ_3[clsdetails[1]]+"_"+test_typ1[clsdetails[2]]
            elif clsdetails[3] == "computermath\n":
                tablename = tablename +dat_typ_4[clsdetails[1]]+"_"+test_typ1[clsdetails[2]]
            elif clsdetails[3] == "commerce\n":
                tablename = tablename +dat_typ_5[clsdetails[1]]+"_"+test_typ1[clsdetails[2]]
        if clsdetails[0][-2] in ("3", "4", "5", "6", "7", "8", "9") and clsdetails[0][-3] == "s" and clsdetails[3] == "stream\n":
            tablename = tablename + dat_typ_2[clsdetails[1]] + "_" + test_typ1[clsdetails[2]]
        if clsdetails[0][-2] in ("1", "2") and clsdetails[0][-3] == "s" and clsdetails[3] == "stream\n":
            tablename = tablename + dat_typ_1[clsdetails[1]] + "_" + test_typ1[clsdetails[2]]
        if clsdetails[0] == "class10\n":
            tablename = tablename + dat_typ_2[clsdetails[1]] + "_" + test_typ2[clsdetails[2]]


        if clsdetails[0] in ("class12\n","class10\n"):
            if clsdetails[2] == "pre\n":
                with open("month_name.txt", 'r') as fh:
                    info = fh.read().strip()
            if clsdetails[2] == "unit\n":
                with open("month_name.txt", 'r') as fh:
                    info = fh.read().strip()
            if clsdetails[2] == "monthly\n":
                with open("month_name.txt", 'r') as fh:
                    info = fh.read().strip()
            tablename = tablename +"_"+info

        print(tablename)
        cmd = "use " + curntyear
        sqlcursor.execute(cmd)
        sqlcursor.execute("show tables")
        qury = sqlcursor.fetchall()
        for item in qury:
            if item[0] == tablename:
                cmd = "delete from " + tablename
                sqlcursor.execute(cmd)
                mydb.commit()
                break
        else:
            cmd = "create table " + tablename + "( rollno varchar(50) , username varchar(50) , marks int)"
            sqlcursor.execute(cmd)

        for i in range(len(rw1)):
            cmd = "insert into " + tablename + "( rollno , username , marks) values('{}','{}',{})".format(rw1[i], rw2[i], rw3[i])
            sqlcursor.execute(cmd)
        mydb.commit()
        self.message_label.setStyleSheet("color: rgb(0,170, 0);font: 12pt 'Arial';")
        self.message_label.setText("The table has been saved")

    def to_refresh(self):

        self.message_label.setText("")


        with open("currentyear.txt",'r') as fh:
            curntyear = fh.read().strip()
        cmd = "use " + curntyear
        sqlcursor.execute(cmd)

        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        if clsdetails[0] == "class1\n":
            tablename1 = curntyear + "_class1_student_table"
        if clsdetails[0] == "class2\n":
            tablename1 = curntyear + "_class2_student_table"
        if clsdetails[0] == "class3\n":
            tablename1 = curntyear + "_class3_student_table"
        if clsdetails[0] == "class4\n":
            tablename1 = curntyear + "_class4_student_table"
        if clsdetails[0] == "class5\n":
            tablename1 = curntyear + "_class5_student_table"
        if clsdetails[0] == "class6\n":
            tablename1 = curntyear + "_class6_student_table"
        if clsdetails[0] == "class7\n":
            tablename1 = curntyear + "_class7_student_table"
        if clsdetails[0] == "class8\n":
            tablename1 = curntyear + "_class8_student_table"
        if clsdetails[0] == "class9\n":
            tablename1 = curntyear + "_class9_student_table"
        if clsdetails[0] == "class10\n":
            tablename1 = curntyear + "_class10_student_table"
        if clsdetails[0] == "class11\n":
            if clsdetails[3] == "biomaths\n":
                tablename1 = curntyear + "_class11_biomaths_student_table"
            elif clsdetails[3] == "computermath\n":
                tablename1 = curntyear + "_class11_compmaths_student_table"
            elif clsdetails[3] == "commerce\n":
                tablename1 = curntyear + "_class11_commerce_student_table"
        if clsdetails[0] == "class12\n":
            if clsdetails[3] == "biomaths\n":
                tablename1 = curntyear + "_class12_biomaths_student_table"
            elif clsdetails[3] == "computermath\n":
                tablename1 = curntyear + "_class12_compmaths_student_table"
            elif clsdetails[3] == "commerce\n":
                tablename1 = curntyear + "_class12_commerce_student_table"

        cmd = "select * from "+tablename1
        print(cmd)
        sqlcursor.execute(cmd)
        val = sqlcursor.fetchall()
        self.tableWidget.setRowCount(len(val))

        for rwcnt in range(len(val)):
            for clmcnt in range(2):
                self.tableWidget.setItem(rwcnt, clmcnt, QtWidgets.QTableWidgetItem(val[rwcnt][clmcnt]))

    def to_prevpg(self):
        with open("classdetails.txt",'r') as fh:
            val = fh.readlines()
        if val[0] in ("class10\n","class12\n"):
            widget.setCurrentIndex(16)
        else:
            widget.setCurrentIndex(7)

class name_collector_for_month(QDialog):
    def __init__(self):
        super(name_collector_for_month, self).__init__()
        loadUi("name_collector_for_month.ui", self)

        self.enter_exe.clicked.connect(self.up_values)
        self.back.clicked.connect(self.to_prevpg)

    def up_values(self):
        val = self.name.text()
        with open("month_name.txt",'w') as fh:
            fh.write(val)

        widget.setCurrentIndex(24)

    def to_prevpg(self):
        widget.setCurrentIndex(16)

class name_collector_for_unit(QDialog):
    def __init__(self):
        super(name_collector_for_unit, self).__init__()
        loadUi("name_collector_for_unit.ui", self)

        self.enter_exe.clicked.connect(self.up_values)
        self.back.clicked.connect(self.to_prevpg)

    def up_values(self):
        val = self.name.text()
        with open("month_name.txt",'w') as fh:
            fh.write(val)

        widget.setCurrentIndex(24)

    def to_prevpg(self):
        widget.setCurrentIndex(16)


class name_collector_for_pre(QDialog):
    def __init__(self):
        super(name_collector_for_pre, self).__init__()
        loadUi("name_collector_for_pre.ui", self)

        self.enter_exe.clicked.connect(self.up_values)
        self.back.clicked.connect(self.to_prevpg)

    def up_values(self):
        val = self.name.text()
        with open("month_name.txt",'w') as fh:
            fh.write(val)

        widget.setCurrentIndex(24)

    def to_prevpg(self):
        widget.setCurrentIndex(16)

class editmarks_selectclass(QDialog):
    def __init__(self):
        super(editmarks_selectclass, self).__init__()
        loadUi("pro_addmarks_main_pg.ui", self)

        self.label_2.setText("Edit Marks")
        self.label_3.setText("Select the class in which marks must be edited to ")

        self.back.clicked.connect(self.to_prevpg)
        self.teacherlogin_class_1.clicked.connect(self.setclass1)
        self.teacherlogin_class_2.clicked.connect(self.setclass2)
        self.teacherlogin_class_3.clicked.connect(self.setclass3)
        self.teacherlogin_class_4.clicked.connect(self.setclass4)
        self.teacherlogin_class_5.clicked.connect(self.setclass5)
        self.teacherlogin_class_6.clicked.connect(self.setclass6)
        self.teacherlogin_class_7.clicked.connect(self.setclass7)
        self.teacherlogin_class_8.clicked.connect(self.setclass8)
        self.teacherlogin_class_9.clicked.connect(self.setclass9)
        self.teacherlogin_class_10.clicked.connect(self.setclass10)
        self.teacherlogin_class_11.clicked.connect(self.setclass11)
        self.teacherlogin_class_12.clicked.connect(self.setclass12)

    def setclass1(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class1\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(29)

    def setclass2(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class2\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(29)

    def setclass3(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class3\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(30)

    def setclass4(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class4\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(30)

    def setclass5(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class5\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(30)

    def setclass6(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class6\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(30)

    def setclass7(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class7\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(30)

    def setclass8(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class8\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(30)

    def setclass9(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class9\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(30)

    def setclass10(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class10\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(30)

    def setclass11(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class11\n", "subject\n", "test\n","stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(31)

    def setclass12(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class12\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(31)

    def to_prevpg(self):
        widget.setCurrentIndex(4)

class editmarks_selectsubject_12(QDialog):
    def __init__(self):
        super(editmarks_selectsubject_12,self).__init__()
        loadUi("pro_addmarks_subject_class12_pg.ui", self)

        self.label_2.setText("Edit Marks")
        self.label_3.setText("Select the subject in which marks must be edited to ")

        self.back_execute.clicked.connect(self.to_prevpg)
        self.teacherlogin_subject_english.clicked.connect(self.seteng)
        self.teacherlogin_subject_evs.clicked.connect(self.setevs)
        self.teacherlogin_subject_maths.clicked.connect(self.setmat)
        self.teacherlogin_subject_lang2.clicked.connect(self.setlan)
        self.teacherlogin_subject_comp.clicked.connect(self.setcom)

    def seteng(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "english\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(32)

    def setevs(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "evs\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(32)

    def setmat(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "maths\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(32)

    def setlan(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "lang2\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(32)

    def setcom(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "computer\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(32)

    def to_prevpg(self):
        widget.setCurrentIndex(28)


class editmarks_selectsubject_345678910(QDialog):
    def __init__(self):
        super(editmarks_selectsubject_345678910, self).__init__()
        loadUi("pro_addmarks_subject_class345678910_pg.ui", self)

        self.label_2.setText("Edit Marks")
        self.label_3.setText("Select the subject in which marks must be edited to ")

        self.back_execute.clicked.connect(self.to_prevpg)
        self.teacherlogin_subject_english.clicked.connect(self.seteng)
        self.teacherlogin_subject_science.clicked.connect(self.setsci)
        self.teacherlogin_subject_maths.clicked.connect(self.setmat)
        self.teacherlogin_subject_lang2.clicked.connect(self.setlan)
        self.teacherlogin_subject_comp.clicked.connect(self.setcom)
        self.teacherlogin_subject_social.clicked.connect(self.setsoc)

    def seteng(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "english\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class10\n":
            widget.setCurrentIndex(36)
        else:
            widget.setCurrentIndex(32)

    def setsci(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "science\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class10\n":
            widget.setCurrentIndex(36)
        else:
            widget.setCurrentIndex(32)

    def setmat(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "maths\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class10\n":
            widget.setCurrentIndex(36)
        else:
            widget.setCurrentIndex(32)


    def setlan(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "lang2\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class10\n":
            widget.setCurrentIndex(36)
        else:
            widget.setCurrentIndex(32)

    def setcom(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "computer\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class10\n":
            widget.setCurrentIndex(36)
        else:
            widget.setCurrentIndex(32)

    def setsoc(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "social\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class10\n":
            widget.setCurrentIndex(36)
        else:
            widget.setCurrentIndex(32)

    def to_prevpg(self):
        widget.setCurrentIndex(28)

class editmarks_select_stream(QDialog):
    def __init__(self):
        super(editmarks_select_stream, self).__init__()
        loadUi("pro_addmarks_stream_pg.ui", self)

        self.label_2.setText("Edit Marks")
        self.label_3.setText("Select the stream in which marks must be edited to ")

        self.back_execute.clicked.connect(self.to_prevpg)
        self.addmarks_stream_biomaths.clicked.connect(self.setbiomaths)
        self.addmarks_stream_computer.clicked.connect(self.setcomputersci)
        self.addmarks_stream_commerce.clicked.connect(self.setcommerce)

    def setbiomaths(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[3] = "biomaths\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(33)

    def setcomputersci(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[3] = "computermath\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(34)

    def setcommerce(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[3] = "commerce\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(35)

    def to_prevpg(self):
        widget.setCurrentIndex(28)

class edit_select_test_typ1_pg(QDialog):
    def __init__(self):
        super(edit_select_test_typ1_pg,self).__init__()
        loadUi("pro_addmarks_exam_type1_pg.ui", self)

        self.label_2.setText("Edit Marks")
        self.label_3.setText("Select the test in which marks must be edited to ")

        self.back_execute.clicked.connect(self.to_prevpg)
        self.teacherlogin_exam_pt1.clicked.connect(self.setpt1)
        self.teacherlogin_exam_pt2.clicked.connect(self.setpt2)
        self.teacherlogin_exam_pt3.clicked.connect(self.setpt3)
        self.teacherlogin_exam_pt4.clicked.connect(self.setpt4)
        self.teacherlogin_subjeteacherlogin_exam_halfyear.clicked.connect(self.sethalfyear)
        self.teacherlogin_exam_annual.clicked.connect(self.setannual)

    def setpt1(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[2] = "periodictest1\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(24)

    def setpt2(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[2] = "periodictest2\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(24)

    def setpt3(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[2] = "periodictest3\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(24)

    def setpt4(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[2] = "periodictest4\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(24)

    def sethalfyear(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[2] = "halfyearly\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(24)

    def setannual(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[2] = "annual\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(24)

    def to_prevpg(self):
        with open("classdetails.txt", "r") as fh:
            cls=fh.readlines()
        if cls[0] in ("class11\n","class12\n"):
            if cls[3] == "biomaths\n":
                widget.setCurrentIndex(33)
            if cls[3] == "computermath\n":
                widget.setCurrentIndex(34)
            if cls[3] == "commerce\n":
                widget.setCurrentIndex(35)
        elif cls[0][-2] in ("3","4","5","6","7","8","9","0",) and cls[0][-3] in ("s","1",):
            widget.setCurrentIndex(8)
        elif cls[0][-2] in ("1","2") and cls[0][-3] in ("s"):
            widget.setCurrentIndex(6)

class editmark_select_subject_biomaths_pg(QDialog):
    def __init__(self):
        super(editmark_select_subject_biomaths_pg,self).__init__()
        loadUi("pro_addmarks_subject_class1211_biomaths_pg.ui", self)

        self.label_2.setText("Edit Marks")
        self.label_3.setText("Select the subject in which marks must be edited to ")

        self.back_execute.clicked.connect(self.to_prevpg)
        self.teacherlogin_subject_english.clicked.connect(self.seteng)
        self.teacherlogin_subject_biology.clicked.connect(self.setbio)
        self.teacherlogin_subject_maths.clicked.connect(self.setmat)
        self.teacherlogin_subject_chemistry.clicked.connect(self.setche)
        self.teacherlogin_subject_physcis.clicked.connect(self.setphy)

    def seteng(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "english\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class12\n":
            widget.setCurrentIndex(36)
        else:
            widget.setCurrentIndex(7)

    def setbio(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "biology\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class12\n":
            widget.setCurrentIndex(36)
        else:
            widget.setCurrentIndex(32)

    def setmat(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "maths\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class12\n":
            widget.setCurrentIndex(36)
        else:
            widget.setCurrentIndex(32)


    def setche(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "chemistry\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class12\n":
            widget.setCurrentIndex(36)
        else:
            widget.setCurrentIndex(32)

    def setphy(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "physics\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class12\n":
            widget.setCurrentIndex(36)
        else:
            widget.setCurrentIndex(32)

    def to_prevpg(self):
        widget.setCurrentIndex(31)


class edit_select_subject_computersci_pg(QDialog):
    def __init__(self):
        super(edit_select_subject_computersci_pg,self).__init__()
        loadUi("pro_addmarks_subject_class1211_compmaths_pg.ui", self)

        self.label_2.setText("Edit Marks")
        self.label_3.setText("Select the subject in which marks must be edited to ")

        self.back_execute.clicked.connect(self.to_prevpg)
        self.teacherlogin_subject_english.clicked.connect(self.seteng)
        self.teacherlogin_subject_computer.clicked.connect(self.setcomp)
        self.teacherlogin_subject_maths.clicked.connect(self.setmat)
        self.teacherlogin_subject_chemistry.clicked.connect(self.setche)
        self.teacherlogin_subject_physcis.clicked.connect(self.setphy)

    def seteng(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "english\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class12\n":
            widget.setCurrentIndex(36)
        else:
            widget.setCurrentIndex(32)


    def setcomp(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "computer\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class12\n":
            widget.setCurrentIndex(36)
        else:
            widget.setCurrentIndex(32)

    def setmat(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "maths\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class12\n":
            widget.setCurrentIndex(36)
        else:
            widget.setCurrentIndex(32)


    def setche(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "chemistry\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class12\n":
            widget.setCurrentIndex(36)
        else:
            widget.setCurrentIndex(32)


    def setphy(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "physics\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class12\n":
            widget.setCurrentIndex(36)
        else:
            widget.setCurrentIndex(32)


    def to_prevpg(self):
        widget.setCurrentIndex(31)


class edit_select_subject_commerce_pg(QDialog):
    def __init__(self):
        super(edit_select_subject_commerce_pg, self).__init__()
        loadUi("pro_addmarks_subject_class1211_commerce_pg.ui", self)

        self.label_2.setText("Edit Marks")
        self.label_3.setText("Select the subject in which marks must be edited to ")

        self.back_execute.clicked.connect(self.to_prevpg)
        self.teacherlogin_subject_english.clicked.connect(self.seteng)
        self.teacherlogin_subject_computer.clicked.connect(self.setcomp)
        self.teacherlogin_subject_buisness.clicked.connect(self.setbuss)
        self.teacherlogin_subject_accounts.clicked.connect(self.setacc)
        self.teacherlogin_subject_economics.clicked.connect(self.seteco)

    def seteng(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "english\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class12\n":
            widget.setCurrentIndex(36)
        else:
            widget.setCurrentIndex(32)


    def setcomp(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "computer\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class12\n":
            widget.setCurrentIndex(36)
        else:
            widget.setCurrentIndex(32)

    def setbuss(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "business\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class12\n":
            widget.setCurrentIndex(36)
        else:
            widget.setCurrentIndex(32)

    def setacc(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "accounts\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class12\n":
            widget.setCurrentIndex(36)
        else:
            widget.setCurrentIndex(32)


    def seteco(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[1] = "economics\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        if clsdetails[0] == "class12\n":
            widget.setCurrentIndex(36)
        else:
            widget.setCurrentIndex(32)

    def to_prevpg(self):
        widget.setCurrentIndex(31)


class edit_select_test_type2(QDialog):
    def __init__(self):
        super(edit_select_test_type2,self).__init__()
        loadUi("pro_addmarks_exam_type2_pg.ui", self)

        self.back_execute.clicked.connect(self.to_prevpg)
        self.teacherlogin_exam_monthly.clicked.connect(self.to_month)
        self.teacherlogin_exam_unit.clicked.connect(self.to_uni)
        self.teacherlogin_exam_preboard.clicked.connect(self.to_pre)

    def to_month(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[2] = "monthly\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(38)

    def to_uni(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[2] = "unit\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(39)

    def to_pre(self):
        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        clsdetails[2] = "pre\n"
        with open("classdetails.txt", 'w') as fh:
            fh.writelines(clsdetails)

        widget.setCurrentIndex(40)

    def to_prevpg(self):
        with open("classdetails.txt", "r") as fh:
            cls = fh.readlines()
        if cls[0] in ("class11\n", "class12\n"):
            if cls[3] == "biomaths\n":
                widget.setCurrentIndex(33)
            if cls[3] == "computermath\n":
                widget.setCurrentIndex(34)
            if cls[3] == "commerce\n":
                widget.setCurrentIndex(35)
        elif cls[0][-2] in ("3", "4", "5", "6", "7", "8", "9", "0",) and cls[0][-3] in ("s", "1",):
            widget.setCurrentIndex(29)
        elif cls[0][-2] in ("1", "2") and cls[0][-3] in ("s"):
            widget.setCurrentIndex(30)

class edit_marks_student_table_pg(QDialog):
    def __init__(self):
        super(edit_marks_student_table_pg,self).__init__()
        loadUi("pro_addmarks_student_table_pg.ui", self)

        self.label_2.setText("Edit Marks")

        self.back.clicked.connect(self.to_prevpg)
        self.refresh.clicked.connect(self.to_refresh)
        self.submit.clicked.connect(self.add_to_db)

    def add_to_db(self):
        rw1 = []
        rw2 = []
        rw3 = []
        rwcount = self.tableWidget.rowCount()
        for rw_no in range(rwcount):
            rw_item = self.tableWidget.item(rw_no, 0).text()
            rw2_item = self.tableWidget.item(rw_no, 1).text()
            rw3_item = self.tableWidget.item(rw_no, 2).text()
            rw1.append(rw_item)
            rw2.append(rw2_item)
            rw3.append(rw3_item)
        with open("currentyear.txt", 'r') as fh:
            curntyear = fh.read().strip()

        dat_typ_1 = {"english\n": "english", "evs\n": "evs", "maths\n": "maths", "lang2\n": "lang2","computer\n": "computer"}
        dat_typ_2 = {"english\n": "english","science\n": "science","social\n": "social","lang2\n": "language","maths\n": "maths", "computer\n": "computer"}
        dat_typ_3 = {"english\n": "english","biology\n": "biology","physics\n": "physics","chemistry\n": "chemistry", "maths\n": "maths"}
        dat_typ_4 = {"english\n": "english","computer\n": "computer","accounts\n": "accounts","economics\n":"economics", "business\n": "business"}
        dat_typ_5 = {"english\n": "english","computer\n": "computer","physics\n": "physics","chemistry\n":"chemistry", "maths\n": "maths"}

        test_typ1 = {"periodictest1\n": "periodic_test_1", "periodictest2\n": "periodic_test_2", "periodictest3\n":"periodic_test_3", "periodictest4\n":"periodic_test_4", "halfyearly\n":"halfyearly", "annual\n":"annual"}
        test_typ2 = {"monthly\n":"monthly","unit\n":"unit","pre\n":"pre"}


        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        if clsdetails[0] == "class1\n":
            tablename = curntyear + "_class1_"
        if clsdetails[0] == "class2\n":
            tablename = curntyear + "_class2_"
        if clsdetails[0] == "class3\n":
            tablename = curntyear + "_class3_"
        if clsdetails[0] == "class4\n":
            tablename = curntyear + "_class4_"
        if clsdetails[0] == "class5\n":
            tablename = curntyear + "_class5_"
        if clsdetails[0] == "class6\n":
            tablename = curntyear + "_class6_"
        if clsdetails[0] == "class7\n":
            tablename = curntyear + "_class7_"
        if clsdetails[0] == "class8\n":
            tablename = curntyear + "_class8_"
        if clsdetails[0] == "class9\n":
            tablename = curntyear + "_class9_"
        if clsdetails[0] == "class10\n":
            tablename = curntyear + "_class10_"
        if clsdetails[0] == "class11\n":
            if clsdetails[3] == "biomaths\n":
                tablename = curntyear + "_class11_biomaths_"
            elif clsdetails[3] == "computermath\n":
                tablename = curntyear + "_class11_compmaths_"
            elif clsdetails[3] == "commerce\n":
                tablename = curntyear + "_class11_commerce_"
        if clsdetails[0] == "class12\n":
            if clsdetails[3] == "biomaths\n":
                tablename = curntyear + "_class12_biomaths_"
            elif clsdetails[3] == "computermath\n":
                tablename = curntyear + "_class12_compmaths_"
            elif clsdetails[3] == "commerce\n":
                tablename = curntyear + "_class12_commerce_"

        if clsdetails[0] in ("class12\n"):
            if clsdetails[3] == "biomaths\n":
                tablename = tablename + dat_typ_3[clsdetails[1]]+"_"+ test_typ2[clsdetails[2]]
            elif clsdetails[3] == "computermath\n":
                tablename = tablename +dat_typ_4[clsdetails[1]]+"_"+test_typ2[clsdetails[2]]
            elif clsdetails[3] == "commerce\n":
                tablename = tablename +dat_typ_5[clsdetails[1]]+"_"+test_typ2[clsdetails[2]]
        if clsdetails[0] in ("class11\n"):
            if clsdetails[3] == "biomaths\n":
                tablename = tablename +dat_typ_3[clsdetails[1]]+"_"+test_typ1[clsdetails[2]]
            elif clsdetails[3] == "computermath\n":
                tablename = tablename +dat_typ_4[clsdetails[1]]+"_"+test_typ1[clsdetails[2]]
            elif clsdetails[3] == "commerce\n":
                tablename = tablename +dat_typ_5[clsdetails[1]]+"_"+test_typ1[clsdetails[2]]
        if clsdetails[0][-2] in ("3", "4", "5", "6", "7", "8", "9") and clsdetails[0][-3] == "s" and clsdetails[3] == "stream\n":
            tablename = tablename + dat_typ_2[clsdetails[1]] + "_" + test_typ1[clsdetails[2]]
        if clsdetails[0][-2] in ("1", "2") and clsdetails[0][-3] == "s" and clsdetails[3] == "stream\n":
            tablename = tablename + dat_typ_1[clsdetails[1]] + "_" + test_typ1[clsdetails[2]]
        if clsdetails[0] == "class10\n":
            tablename = tablename + dat_typ_2[clsdetails[1]] + "_" + test_typ2[clsdetails[2]]


        if clsdetails[0] in ("class12\n","class10\n"):
            if clsdetails[2] == "pre\n":
                with open("month_name.txt", 'r') as fh:
                    info = fh.read().strip()
            if clsdetails[2] == "unit\n":
                with open("month_name.txt", 'r') as fh:
                    info = fh.read().strip()
            if clsdetails[2] == "monthly\n":
                with open("month_name.txt", 'r') as fh:
                    info = fh.read().strip()
            tablename = tablename +"_"+info

        print(tablename)
        cmd = "use " + curntyear
        sqlcursor.execute(cmd)
        sqlcursor.execute("show tables")
        qury = sqlcursor.fetchall()
        for item in qury:
            if item[0] == tablename:
                cmd = "delete from " + tablename
                sqlcursor.execute(cmd)
                mydb.commit()
                break
        else:
            cmd = "create table " + tablename + "( rollno varchar(50) , username varchar(50) , marks int)"
            sqlcursor.execute(cmd)

        for i in range(len(rw1)):
            cmd = "insert into " + tablename + "( rollno , username , marks) values('{}','{}',{})".format(rw1[i], rw2[i], rw3[i])
            sqlcursor.execute(cmd)
        mydb.commit()
        self.message_label.setStyleSheet("color: rgb(0,170, 0);font: 12pt 'Arial';")
        self.message_label.setText("The table has been edited")

    def to_refresh(self):

        self.message_label.setText("")

        with open("currentyear.txt",'r') as fh:
            curntyear = fh.read().strip()
        cmd = "use " + curntyear
        sqlcursor.execute(cmd)

        dat_typ_1 = {"english\n": "english", "evs\n": "evs", "maths\n": "maths", "lang2\n": "lang2",
                     "computer\n": "computer"}
        dat_typ_2 = {"english\n": "english", "science\n": "science", "social\n": "social", "lang2\n": "language",
                     "maths\n": "maths", "computer\n": "computer"}
        dat_typ_3 = {"english\n": "english", "biology\n": "biology", "physics\n": "physics", "chemistry\n": "chemistry",
                     "maths\n": "maths"}
        dat_typ_4 = {"english\n": "english", "computer\n": "computer", "accounts\n": "accounts",
                     "economics\n": "economics", "business\n": "business"}
        dat_typ_5 = {"english\n": "english", "computer\n": "computer", "physics\n": "physics",
                     "chemistry\n": "chemistry", "maths\n": "maths"}

        test_typ1 = {"periodictest1\n": "periodic_test_1", "periodictest2\n": "periodic_test_2",
                     "periodictest3\n": "periodic_test_3", "periodictest4\n": "periodic_test_4",
                     "halfyearly\n": "halfyearly", "annual\n": "annual"}
        test_typ2 = {"monthly\n": "monthly", "unit\n": "unit", "pre\n": "pre"}

        with open("classdetails.txt", 'r') as fh:
            clsdetails = fh.readlines()
        if clsdetails[0] == "class1\n":
            tablename = curntyear + "_class1_"
        if clsdetails[0] == "class2\n":
            tablename = curntyear + "_class2_"
        if clsdetails[0] == "class3\n":
            tablename = curntyear + "_class3_"
        if clsdetails[0] == "class4\n":
            tablename = curntyear + "_class4_"
        if clsdetails[0] == "class5\n":
            tablename = curntyear + "_class5_"
        if clsdetails[0] == "class6\n":
            tablename = curntyear + "_class6_"
        if clsdetails[0] == "class7\n":
            tablename = curntyear + "_class7_"
        if clsdetails[0] == "class8\n":
            tablename = curntyear + "_class8_"
        if clsdetails[0] == "class9\n":
            tablename = curntyear + "_class9_"
        if clsdetails[0] == "class10\n":
            tablename = curntyear + "_class10_"
        if clsdetails[0] == "class11\n":
            if clsdetails[3] == "biomaths\n":
                tablename = curntyear + "_class11_biomaths_"
            elif clsdetails[3] == "computermath\n":
                tablename = curntyear + "_class11_compmaths_"
            elif clsdetails[3] == "commerce\n":
                tablename = curntyear + "_class11_commerce_"
        if clsdetails[0] == "class12\n":
            if clsdetails[3] == "biomaths\n":
                tablename = curntyear + "_class12_biomaths_"
            elif clsdetails[3] == "computermath\n":
                tablename = curntyear + "_class12_compmaths_"
            elif clsdetails[3] == "commerce\n":
                tablename = curntyear + "_class12_commerce_"

        if clsdetails[0] in ("class12\n"):
            if clsdetails[3] == "biomaths\n":
                tablename = tablename + dat_typ_3[clsdetails[1]] + "_" + test_typ2[clsdetails[2]]
            elif clsdetails[3] == "computermath\n":
                tablename = tablename + dat_typ_4[clsdetails[1]] + "_" + test_typ2[clsdetails[2]]
            elif clsdetails[3] == "commerce\n":
                tablename = tablename + dat_typ_5[clsdetails[1]] + "_" + test_typ2[clsdetails[2]]
        if clsdetails[0] in ("class11\n"):
            if clsdetails[3] == "biomaths\n":
                tablename = tablename + dat_typ_3[clsdetails[1]] + "_" + test_typ1[clsdetails[2]]
            elif clsdetails[3] == "computermath\n":
                tablename = tablename + dat_typ_4[clsdetails[1]] + "_" + test_typ1[clsdetails[2]]
            elif clsdetails[3] == "commerce\n":
                tablename = tablename + dat_typ_5[clsdetails[1]] + "_" + test_typ1[clsdetails[2]]
        if clsdetails[0][-2] in ("3", "4", "5", "6", "7", "8", "9") and clsdetails[0][-3] == "s" and clsdetails[
            3] == "stream\n":
            tablename = tablename + dat_typ_2[clsdetails[1]] + "_" + test_typ1[clsdetails[2]]
        if clsdetails[0][-2] in ("1", "2") and clsdetails[0][-3] == "s" and clsdetails[3] == "stream\n":
            tablename = tablename + dat_typ_1[clsdetails[1]] + "_" + test_typ1[clsdetails[2]]
        if clsdetails[0] == "class10\n":
            tablename = tablename + dat_typ_2[clsdetails[1]] + "_" + test_typ2[clsdetails[2]]

        if clsdetails[0] in ("class12\n", "class10\n"):
            if clsdetails[2] == "pre\n":
                with open("month_name.txt", 'r') as fh:
                    info = fh.read().strip()
            if clsdetails[2] == "unit\n":
                with open("month_name.txt", 'r') as fh:
                    info = fh.read().strip()
            if clsdetails[2] == "monthly\n":
                with open("month_name.txt", 'r') as fh:
                    info = fh.read().strip()
            tablename = tablename + "_" + info

        cmd = "select * from "+tablename
        sqlcursor.execute(cmd)
        val = sqlcursor.fetchall()
        self.tableWidget.setRowCount(len(val))

        for rwcnt in range(len(val)):
            for clmcnt in range(3):
                print(val[rwcnt][clmcnt])
                self.tableWidget.setItem(rwcnt, clmcnt, QtWidgets.QTableWidgetItem(str(val[rwcnt][clmcnt])))

    def to_prevpg(self):
        with open("classdetails.txt",'r') as fh:
            val = fh.readlines()
        if val[0] in ("class10\n","class12\n"):
            widget.setCurrentIndex(36)
        else:
            widget.setCurrentIndex(32)

class edit_name_collector_for_month(QDialog):
    def __init__(self):
        super(edit_name_collector_for_month, self).__init__()
        loadUi("name_collector_for_month.ui", self)

        self.label_2.setText("Edit Marks")

        self.enter_exe.clicked.connect(self.up_values)
        self.back.clicked.connect(self.to_prevpg)

    def up_values(self):
        val = self.name.text()
        with open("month_name.txt",'w') as fh:
            fh.write(val)

        widget.setCurrentIndex(37)

    def to_prevpg(self):
        widget.setCurrentIndex(36)

class edit_name_collector_for_unit(QDialog):
    def __init__(self):
        super(edit_name_collector_for_unit, self).__init__()
        loadUi("name_collector_for_unit.ui", self)

        self.label_2.setText("Edit Marks")

        self.enter_exe.clicked.connect(self.up_values)
        self.back.clicked.connect(self.to_prevpg)

    def up_values(self):
        val = self.name.text()
        with open("month_name.txt",'w') as fh:
            fh.write(val)

        widget.setCurrentIndex(37)

    def to_prevpg(self):
        widget.setCurrentIndex(36)


class edit_name_collector_for_pre(QDialog):
    def __init__(self):
        super(edit_name_collector_for_pre, self).__init__()
        loadUi("name_collector_for_pre.ui", self)

        self.label_2.setText("Edit Marks")

        self.enter_exe.clicked.connect(self.up_values)
        self.back.clicked.connect(self.to_prevpg)

    def up_values(self):
        val = self.name.text()
        with open("month_name.txt",'w') as fh:
            fh.write(val)

        widget.setCurrentIndex(37)

    def to_prevpg(self):
        widget.setCurrentIndex(36)

class cls_progress_main_pg(QDialog):
    def __init__(self):
        super(cls_progress_main_pg, self).__init__()
        loadUi("pro_addmarks_main_pg.ui", self)

        self.label_2.setText("Class Progress")
        self.label_3.setText("Select the class to check its progress")

        self.back.clicked.connect(self.to_prevpg)
        self.teacherlogin_class_1.clicked.connect(self.setclass1)
        self.teacherlogin_class_2.clicked.connect(self.setclass2)
        self.teacherlogin_class_3.clicked.connect(self.setclass3)
        self.teacherlogin_class_4.clicked.connect(self.setclass4)
        self.teacherlogin_class_5.clicked.connect(self.setclass5)
        self.teacherlogin_class_6.clicked.connect(self.setclass6)
        self.teacherlogin_class_7.clicked.connect(self.setclass7)
        self.teacherlogin_class_8.clicked.connect(self.setclass8)
        self.teacherlogin_class_9.clicked.connect(self.setclass9)
        self.teacherlogin_class_10.clicked.connect(self.setclass10)
        self.teacherlogin_class_11.clicked.connect(self.setclass11)
        self.teacherlogin_class_12.clicked.connect(self.setclass12)

    def setclass1(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class1\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(6)

    def setclass2(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class2\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(6)

    def setclass3(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class3\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(8)

    def setclass4(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class4\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(8)

    def setclass5(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class5\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(8)

    def setclass6(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class6\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(8)

    def setclass7(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class7\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(8)

    def setclass8(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class8\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(8)

    def setclass9(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class9\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(8)

    def setclass10(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class10\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(8)

    def setclass11(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class11\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(9)

    def setclass12(self):
        with open("classdetails.txt", 'w') as fh:
            clsdetails = (["class12\n", "subject\n", "test\n", "stream\n"])
            fh.writelines(clsdetails)
        widget.setCurrentIndex(9)

    def to_prevpg(self):
        widget.setCurrentIndex(4)

















with open("notice.txt",'r') as fh:
    line = fh.readlines()
    if len(line) == 0:
        with open("notice.txt",'w') as fh1:
            data = '''Welcome to mark register
            the notice will be soon added once someone adds it'''
            fh1.write(data)

def easteregg():
    tablename = "year2022_class12_compmaths_computer_monthly_may"
    sqlcursor.execute("show databases")
    qury = sqlcursor.fetchall()
    for item in qury:
        if item[0] == "year2022":
            break
    else:
        sqlcursor.execute("create database year2022")

    sqlcursor.execute("use year2022")
    sqlcursor.execute("show tables")
    qury = sqlcursor.fetchall()
    for item in qury:
        if item[0] == "year2022_class12_compmaths_computer_monthly_may":
            break
    else:
        cmd = "create table " + tablename + "( rollno varchar(50) , username varchar(50) , marks int)"
        sqlcursor.execute(cmd)

    rw1 = ["1201","1202","1203","1204","1205","1206","1207","1208","1209","1210","1211","12012"]
    rw2 = ["deepak N", "deepak choyal", "hanuram", "hemapraveen", "rithwik", "sahil", "afrin sahana", "deeppika", "divya", "monika", "puspha" , "yogitha" ]
    rw3 = ["100", "100", "100", "100", "100", "100", "100", "100", "100", "100", "100", "100" ]
    for i in range(len(rw1)):
        cmd = "insert into " + tablename + "( rollno , username , marks) values('{}','{}',{})".format(rw1[i], rw2[i],rw3[i])
        sqlcursor.execute(cmd)
    mydb.commit

easteregg()

app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
mainwindow = login_pg()
master_main_pg = master_main_pg()
add_participant = add_participant()
remove_participant = remove_participant()
staff_login_main_pg = staff_login_main_pg()
addmarks_selectclass = addmarks_selectclass()
addmarks_selectsubject_12 = addmarks_selectsubject_12()
addmarks_selectsubject_345678910 = addmarks_selectsubject_345678910()
select_test_typ1_pg = select_test_typ1_pg()
addmarks_select_stream = addmarks_select_stream()
select_subject_biomaths_pg = select_subject_biomaths_pg()
select_subject_computersci_pg = select_subject_computersci_pg()
select_subject_commerce_pg = select_subject_commerce_pg()
additional_settings_pg = additional_settings_pg()
change_password_pg = change_password_pg()
set_notice = set_notice()
select_test_type2 = select_test_type2()
edit_participant = edit_participant()
edit_participant_select_stream = edit_participant_select_stream()
edit_participant_select_table =  edit_participant_select_table()
edit_participant_teacher_table = edit_participant_teacher_table()
pro_set_year_pg = pro_set_year_pg()
pro_editpart_student_no_pg = pro_editpart_student_no_pg()
pro_editpart_student_table_pg = pro_editpart_student_table_pg()
pro_addmarks_student_table_pg = pro_addmarks_student_table_pg()
name_collector_for_month = name_collector_for_month()
name_collector_for_unit = name_collector_for_unit()
name_collector_for_pre = name_collector_for_pre()
editmarks_selectclass = editmarks_selectclass()
editmarks_selectsubject_12 = editmarks_selectsubject_12()
editmarks_selectsubject_345678910 = editmarks_selectsubject_345678910()
editmarks_select_stream = editmarks_select_stream()
edit_select_test_typ1_pg = edit_select_test_typ1_pg()
editmark_select_subject_biomaths_pg = editmark_select_subject_biomaths_pg()
edit_select_subject_computersci_pg = edit_select_subject_computersci_pg()
edit_select_subject_commerce_pg = edit_select_subject_commerce_pg()
edit_select_test_type2 = edit_select_test_type2()
edit_marks_student_table_pg = edit_marks_student_table_pg()
edit_name_collector_for_month = edit_name_collector_for_month()
edit_name_collector_for_unit = edit_name_collector_for_unit()
edit_name_collector_for_pre = edit_name_collector_for_pre()
cls_progress_main_pg = cls_progress_main_pg()
widget.addWidget(mainwindow)# index = 0
widget.addWidget(master_main_pg)# index = 1
widget.addWidget(add_participant)# index = 2
widget.addWidget(remove_participant)# index = 3
widget.addWidget(staff_login_main_pg)# index = 4
widget.addWidget(addmarks_selectclass)# index = 5
widget.addWidget(addmarks_selectsubject_12)# index = 6
widget.addWidget(select_test_typ1_pg)# index = 7
widget.addWidget(addmarks_selectsubject_345678910)# index = 8
widget.addWidget(addmarks_select_stream)# index = 9
widget.addWidget(select_subject_biomaths_pg)# index = 10
widget.addWidget(select_subject_computersci_pg)# index = 11
widget.addWidget(select_subject_commerce_pg)# index = 12
widget.addWidget(additional_settings_pg)# index = 13
widget.addWidget(change_password_pg)# index = 14
widget.addWidget(set_notice)# index = 15
widget.addWidget(select_test_type2)# index = 16
widget.addWidget(edit_participant)# index = 17
widget.addWidget(edit_participant_select_stream)# index = 18
widget.addWidget(edit_participant_select_table)# index = 19
widget.addWidget(edit_participant_teacher_table)# index = 20
widget.addWidget(pro_set_year_pg)# index = 21
widget.addWidget(pro_editpart_student_no_pg)# index = 22
widget.addWidget(pro_editpart_student_table_pg)# index = 23
widget.addWidget(pro_addmarks_student_table_pg)# index = 24
widget.addWidget(name_collector_for_month)# index = 25
widget.addWidget(name_collector_for_unit)# index = 26
widget.addWidget(name_collector_for_pre)# index = 27
widget.addWidget(editmarks_selectclass)# index = 28
widget.addWidget(editmarks_selectsubject_12)# index = 29
widget.addWidget(editmarks_selectsubject_345678910)# index = 30
widget.addWidget(editmarks_select_stream)# index = 31
widget.addWidget(edit_select_test_typ1_pg)# index = 32
widget.addWidget(editmark_select_subject_biomaths_pg)# index = 33
widget.addWidget(edit_select_subject_computersci_pg)# index = 34
widget.addWidget(edit_select_subject_commerce_pg)# index = 35
widget.addWidget(edit_select_test_type2)# index = 36
widget.addWidget(edit_marks_student_table_pg)# index = 37
widget.addWidget(edit_name_collector_for_month)# index = 38
widget.addWidget(edit_name_collector_for_unit)# index = 39
widget.addWidget(edit_name_collector_for_pre)# index = 40
widget.addWidget(cls_progress_main_pg)# index = 41
widget.show()


try:
    sys.exit(app.exec_())
except:
    print("exiting")
    with open("classdetails.txt", "r") as fh:
        print(fh.read())



