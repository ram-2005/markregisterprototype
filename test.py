<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>545</width>
    <height>600</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QLabel" name="label">
    <property name="geometry">
     <rect>
      <x>50</x>
      <y>10</y>
      <width>271</width>
      <height>261</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <family>Neuropol</family>
      <pointsize>22</pointsize>
     </font>
    </property>
    <property name="text">
     <string>TextLabel</string>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>545</width>
     <height>21</height>
    </rect>
   </property>
   <widget class="QMenu" name="menuFILE">
    <property name="title">
     <string>FILE</string>
    </property>
    <addaction name="actionNEW"/>
   </widget>
   <widget class="QMenu" name="menuEDIT">
    <property name="title">
     <string>EDIT</string>
    </property>
    <addaction name="actionCOPY"/>
    <addaction name="actionPASTE"/>
   </widget>
   <addaction name="menuFILE"/>
   <addaction name="menuEDIT"/>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
  <action name="actionEDIT">
   <property name="text">
    <string>EDIT</string>
   </property>
  </action>
  <action name="actionNEW">
   <property name="text">
    <string>NEW</string>
   </property>
  </action>
  <action name="actionCOPY">
   <property name="text">
    <string>COPY </string>
   </property>
  </action>
  <action name="actionPASTE">
   <property name="text">
    <string>PASTE</string>
   </property>
  </action>
 </widget>
 <resources/>
 <connections/>
</ui>
