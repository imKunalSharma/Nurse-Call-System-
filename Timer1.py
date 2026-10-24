import asyncio
import serial
import sys
import configparser
import os.path
import os
import shutil
import csv
import time
import alsaaudio
#Libraries
import RPi.GPIO as GPIO
from time import sleep

from os import path
from csv import writer

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0
from typing import Iterator, Tuple
from serial.tools.list_ports import comports
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import  QWidget, QLabel, QComboBox, QGridLayout, QGroupBox,  \
    QPushButton, QMessageBox, QApplication, QLineEdit, QPlainTextEdit, QMainWindow, QHBoxLayout
from PyQt5.QtGui import QCloseEvent, QFont, QPixmap ,QPainter, QColor, QFont ,QPen
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QImage, QPalette
from quamash import QEventLoop
from PyQt5.QtCore import QSize,Qt
from PyQt5 import QtCore
# Object for access to the serial port
ser = serial.Serial(timeout=0)
SER_BAUDRATE = 9600

# Setting constants
SETTING_PORT_NAME = 'port_name'
SETTING_MESSAGE = 'message'


def gen_serial_ports() -> Iterator[Tuple[str, str]]:
    """Return all available serial ports."""
    ports = comports()
    return ((p.description, p.device) for p in ports)


def send_serial_async(msg: str) -> None:
    """Send a message to serial port (async)."""
    ser.write(msg.encode())

def timerEvent():
        global time
        time = time.addSecs(1)
      #  x=MainWindow(self)
      #  x.update_label(self,time)
        print(time.toString("hh:mm:ss"))
        MainWindow.update_label("1")        
       # MainWindow.label2=QLabel("0002",MainWindow)
       
# noinspection PyArgumentList
"""
class RemoteWidget(QWidget):
    #Main Widget.

    def __init__(self, parent: QWidget=None) -> None:
        super().__init__(parent)
        self.setMinimumSize(QSize(1400, 700))  
        #self.port_label = QLabel(self.tr('COM Port:'))
        
        self.port_combobox = QComboBox()
        self.port_label.setBuddy(self.port_combobox)
        self.update_com_ports()
        
        layout = QGridLayout()
        #layout.addWidget(self.port_label,0,-1)
        #self.port_label.move(1200,100)
        self.label1=QLabel("Select Com Port",self)
        self.label1.move(10,50)
        self.connect_btn = QPushButton('Connect')
        self.connect_btn.move(500,55)
        self.port_combobox.move(50,100)
        
       # self.setLayout(layout)
        
        
        
    def update_com_ports(self) -> None:
        #Update COM Port list in GUI.
        for name, device in gen_serial_ports():
            self.port_combobox.addItem(name, device)
"""
        

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        if os.stat("/home/pi/NewFolder/testing/db.ini").st_size==0:
            shutil.copyfile("/home/pi/NewFolder/testing/db file backup/db.ini", "/home/pi/NewFolder/testing/db.ini")
    
        if os.stat("/home/pi/Share_Folder/my.ini").st_size==0:
            shutil.copyfile("/home/pi/NewFolder/testing/db file backup/my.ini", "/home/pi/Share_Folder/my.ini")
        
        #for volume up down
        self.m = alsaaudio.Mixer()
        vol4 = self.m.setvolume(100)
        
        # instantiate
        config = ConfigParser()
        self.config1 = ConfigParser()
        
        
        self.setStyleSheet("background-color: white")
        #self.setMinimumSize(QSize(1020, 800))
        self.setGeometry(0,-1,1440,900)
        #self.port_label = QLabel('All Com Port',self)
        
        self.port_combobox = QComboBox(self)
        #self.port_label.setBuddy(self.port_combobox)
        self.update_com_ports()
        self.timeval=0
        layout = QGridLayout()
        #layout.addWidget(self.port_label,0,-1)
        #self.port_label.move(1200,100)
        self.label1=QLabel("Port No.",self)
        self.label1.resize(140,20)
        self.label1.move(5,780)
        self.label1.setStyleSheet("font-size:15px; font-weight:bold; qproperty-alignment: AlignCenter;")
        #self.label1.hide()
        
        self.lb_com=QLabel(self)
        self.lb_com.resize(140,20)
        self.lb_com.move(5,800)
        self.lb_com.setStyleSheet("font-size:15px; qproperty-alignment: AlignCenter;")
        
        self.lb_wing=QLabel(self)
        self.lb_wing.resize(300,32)
        self.lb_wing.move(570,5)
        self.lb_wing.setFont(QFont('Times', 20))
        self.lb_wing.setStyleSheet("color: #357EC7; qproperty-alignment: AlignCenter; font-weight: bold")
        
        self.lb_msg_lb=QLabel("IP STATUS", self)
        self.lb_msg_lb.resize(140,32)
        self.lb_msg_lb.move(5,690)
        self.lb_msg_lb.setFont(QFont('Times', 20))
        self.lb_msg_lb.setStyleSheet("font-size:20px; font-weight:bold; qproperty-alignment: AlignCenter;")
        
        self.lb_Mute=QLabel("Mute Off", self)
        self.lb_Mute.resize(140,40)
        self.lb_Mute.move(5,590)
        self.lb_Mute.setStyleSheet("color: white; font-size:20px; qproperty-alignment: AlignCenter; font-weight: bold; Background-color: Green; border-radius: 10px;")
        
        
        self.lb_msg=QLabel(self)
        self.lb_msg.resize(50,45)
        self.lb_msg.move(50,720)
        self.lb_msg.setStyleSheet("font-size:20px;")
        self.image2 = QImage("./light.png")
        self.imagepix2 = QPixmap.fromImage(self.image2)
        self.lb_msg.setScaledContents(True)
        self.lb_msg.setPixmap(self.imagepix2)
        
        self.lb_clock=QLabel(self)
        self.lb_clock.resize(75,80)
        self.lb_clock.move(35,270)
        self.lb_clock.setStyleSheet("font-size:20px;")
        self.image3 = QImage("./clock.png")
        self.imagepix3 = QPixmap.fromImage(self.image3)
        self.lb_clock.setScaledContents(True)
        self.lb_clock.setPixmap(self.imagepix3)
        
        self.lb_thank=QLabel(self)
        self.lb_thank.resize(75,80)
        self.lb_thank.move(750,820)
        self.lb_thank.setStyleSheet("font-size:20px;")
        self.image_th = QImage("./thankyou.png")
        self.imagepix_th = QPixmap.fromImage(self.image_th)
        self.lb_thank.setScaledContents(True)
        self.lb_thank.setPixmap(self.imagepix_th)
        
        
        
        self.connect_btn = QPushButton('Connect',self)
        self.connect_btn.move(5,300)
        self.connect_btn.clicked.connect(self.on_connect_btn_pressed)
        self.connect_btn.setStyleSheet("* {color: white;"
                       "background: qlineargradient( x1:0 y1:0, x2:0 y2:1, stop:0 rgb(84, 158, 151), stop:1 rgb(10, 33, 31));}");
        self.connect_btn.resize(90,32)
        self.connect_btn.hide()

        #self.connect_btn.move(250,55)
        self.disconnect_btn = QPushButton('Disconnect',self)
        self.disconnect_btn.clicked.connect(self.on_disconnect_btn_pressed)
        self.disconnect_btn.move(5,300)
        self.disconnect_btn.setVisible(False)
        #self.disconnect_btn.hide()

        #self.connect_btn.setStyleSheet("* {color: white;background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 2189,stop: 0.1 2462, stop: 0.49 1916,border-width: 1px;border-color: 339;border-style: solid;border-radius: 7;padding: 3px;font-size: 10px;padding-left: 5px;padding-right: 5px;min-width: 50px;max-width: 50px;min-height: 13px;max-height: 13px);}"))
        self.port_combobox.move(5,250)
        self.port_combobox.resize(90,32)
        self.port_combobox.hide()
        
        self.msg_lineedit = QLineEdit(self) #text box name msg_lineedit
        self.msg_lineedit.move(5, 350)
        self.msg_lineedit.resize(90,32)
        self.msg_lineedit.setEnabled(False)
        self.msg_lineedit.hide()
        
        self.send_btn = QPushButton('Send',self)
        self.send_btn.clicked.connect(self.on_send_btn_pressed)
        self.send_btn.move(5,400)
        self.send_btn.resize(90,32) 
        self.send_btn.setStyleSheet("* {color: white;"
                       "background: qlineargradient( x1:0 y1:0, x2:0 y2:1, stop:0 cyan, stop:1 blue);}");
        self.send_btn.hide()
          
        self.report_btn = QPushButton('Report',self)
        #self.report_btn.clicked.connect(self.on_send_btn_pressed)
        self.report_btn.move(10,200)
        self.report_btn.resize(80,32)
        self.report_btn.setStyleSheet("* {color: white; font-weight: bold;"
                       "background: qlineargradient( x1:0 y1:0, x2:0 y2:1, stop:0 cyan, stop:1 blue);}");
        self.report_btn.hide()
        
        self.addphone_btn = QPushButton('AddPhone\nNo',self)
        #self.report_btn.clicked.connect(self.on_send_btn_pressed)
        self.addphone_btn.move(10,270)
        self.addphone_btn.resize(80,62)
        self.addphone_btn.hide()

        self.addphone_btn.setStyleSheet("* {color: white; font-weight: bold;"
                       "background: qlineargradient( x1:0 y1:0, x2:0 y2:1, stop:0 cyan, stop:1 blue);}");
      
        
        
        self.count_blinker=0
        
        
        #QLabel* m_boardLbArray[8]
       # for x in range (1,5): 
        #self.label2=QLabel("0001",self)
        #self.label2.setAlignment(Qt.AlignCenter)
        #self.label2.resize(80,32) 
        #self.label2.setFont(QFont('DS-Digital', 30))
        #self.label2.setStyleSheet("background-color: #FFFFDE")
        #self.label2.move(150,200)
       
        #Disable warnings (optional)
        GPIO.setwarnings(True)
        #Select GPIO mode
        GPIO.setmode(GPIO.BCM)
        #Set buzzer - pin 23 as output
        self.buzzer=23
        self.comnunication=24
        GPIO.setup(self.buzzer,GPIO.OUT)
        GPIO.setup(self.comnunication,GPIO.OUT)
        #Switch Button
        self.switch_count=0
        self.btn_press=0
        self.switch=25
        GPIO.setup(self.switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
       
        self.comm_blink=0
        self.nor_blink=0
        self.em_blink=0
        
        self.blink=0
        self.count = 0
        self.text1 = ''
        config.read("db.ini")
        self.config1.read("db.ini")
        
        self.wing=config['Wing_Name'].get('name')
        self.lb_wing.setText(self.wing)
        
        
        
        #print(value3)
        self.total_bed=0
        self.buzzer_flag=0
        self.total_bed=config['Total_Bed'].getint('total')
        value2 = config['Total_Bed'].get('bed1name') #sections()
        self.value2 = self.config1['Total_Bed'].get('bed1name') #sections()
        self.com = config['Com'].get('port')
        self.lb_com.setText(self.com)
        
        self.controller_max_id = self.config1['Controller'].get('max_id')

        self.label_c_blue=QLabel("",self)
        self.label_c_blue.move(160,780)
        self.label_c_blue.resize(1275,45)
        self.label_c_blue.setFont(QFont('Times', 35))
        #self.label_c_blue.setStyleSheet("color: black; Background-color: cyan; background:QLinearGradient(#005aaa,white,#005aaa);  qproperty-alignment: AlignCenter; font-weight: bold")
        #self.label_c_blue.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(61, 217, 245), stop:1 rgb(0, 53, 218)); qproperty-alignment: AlignCenter; font-weight: bold"); 
        self.label_c_blue.setStyleSheet("background-color: cyan; qproperty-alignment: AlignCenter; font-weight: bold; color:blue")
        #print(self.com)
        #######################################################
        if ser.is_open:
            ser.close()
        ser.port = self.com#"/dev/ttyUSB0"
        ser.baudrate = SER_BAUDRATE
        #print("port details :"+str(ser.port)+" " + str(ser.baudrate))
        try:
            ser.open()
        except Exception as e:
            self.show_error_message(str(e))

        if ser.is_open:
            #self.connect_btn.setVisible(False)
            #self.disconnect_btn.setVisible(True)
            #self.port_combobox.setDisabled(True)
            #self.msg_lineedit.setEnabled(True)
            #self.send_btn.setEnabled(True)
            loop.create_task(self.receive_serial_async())
        ######################################################
        #print(total_bed)
        self.array_str=[40]
        self.status_arr=[40]
        self.flag_arr=[40]
                       
        self.countLoop=0                    
        for i in range(1,33):
            self.array_str.append(config['Total_Bed'].get("bed" + str(i) + "name"))
            self.status_arr.append("0")
            self.flag_arr.append("0")
            
            #self.array_str.insert(0,"0")
            print(self.array_str[i])
            
        #array_str[6]="0"
        #print(array_str[6])
        
        self.config2 = ConfigParser()
        self.config2.read("/home/pi/Share_Folder/my.ini")
        #self.value = self.config2.sections()
        #print(self.value)
        
        lb_font = QFont('DS-Digital', 40)
        #lb_font = QFont('Times', 40)
        lb_font.setWeight(100)
        
        
        
        #First
        if(self.total_bed>0):
            value2 = config['Total_Bed'].get('bed1name')
            self.Bed01=QLabel(value2,self)
            self.Bed01.resize(200, 95)
            self.Bed01.setFont(lb_font)
            self.Bed01.move(180,180)
            
            
        if(self.total_bed>1):
            value2 = config['Total_Bed'].get('bed2name')
            self.Bed02=QLabel(value2,self)
            self.Bed02.resize(200, 95)
            self.Bed02.setFont(lb_font)
            self.Bed02.move(385,180)
            
        if(self.total_bed>2):
            value2 = config['Total_Bed'].get('bed3name')
            self.Bed03=QLabel(value2,self)
            self.Bed03.setFont(lb_font)
            self.Bed03.resize(200, 95)
            self.Bed03.move(590,180)
        if(self.total_bed>3):
            value2 = config['Total_Bed'].get('bed4name')
            self.Bed04=QLabel(value2,self)
            self.Bed04.setFont(lb_font)
            self.Bed04.resize(200, 95)
            self.Bed04.move(795,180)
        if(self.total_bed>4):
            value2 = config['Total_Bed'].get('bed5name')
            self.Bed05=QLabel(value2,self)
            self.Bed05.setFont(lb_font)
            self.Bed05.resize(200, 95)
            self.Bed05.move(1000,180)
        if(self.total_bed>5):
            value2 = config['Total_Bed'].get('bed6name')
            self.Bed06=QLabel(value2,self)
            self.Bed06.resize(200, 95)
            self.Bed06.setFont(lb_font)
            self.Bed06.move(1205,180)
        if(self.total_bed>6):
            value2 = config['Total_Bed'].get('bed7name')
            self.Bed07=QLabel(value2,self)
            self.Bed07.setFont(lb_font)
            self.Bed07.resize(200, 95)
            self.Bed07.move(180,280)
        if(self.total_bed>7):
            value2 = config['Total_Bed'].get('bed8name')
            self.Bed08=QLabel(value2,self)
            self.Bed08.setFont(lb_font)
            self.Bed08.resize(200, 95)
            self.Bed08.move(385,280)
        if(self.total_bed>8):
            value2 = config['Total_Bed'].get('bed9name')
            self.Bed09=QLabel(value2,self)
            self.Bed09.setFont(lb_font)
            self.Bed09.resize(200, 95)
            self.Bed09.move(590,280)
        if(self.total_bed>9):
            value2 = config['Total_Bed'].get('bed10name')
            self.Bed10=QLabel(value2,self)
            self.Bed10.setFont(lb_font)
            self.Bed10.resize(200, 95)
            self.Bed10.move(795,280)
        if(self.total_bed>10):
            value2 = config['Total_Bed'].get('bed11name')
            self.Bed11=QLabel(value2,self)
            self.Bed11.setFont(lb_font)
            self.Bed11.resize(200, 95)
            self.Bed11.move(1000,280)
        if(self.total_bed>11):
            value2 = config['Total_Bed'].get('bed12name')
            self.Bed12=QLabel(value2,self)
            self.Bed12.resize(200, 95)
            self.Bed12.setFont(lb_font)
            self.Bed12.move(1205,280)
        if(self.total_bed>12):
            value2 = config['Total_Bed'].get('bed13name')
            self.Bed13=QLabel(value2,self)
            self.Bed13.resize(200, 95)
            self.Bed13.setFont(lb_font)
            self.Bed13.move(180,380)
        if(self.total_bed>13):
            value2 = config['Total_Bed'].get('bed14name')
            self.Bed14=QLabel(value2,self)
            self.Bed14.setFont(lb_font)
            self.Bed14.resize(200, 95)
            self.Bed14.move(385,380)
        if(self.total_bed>14):
            value2 = config['Total_Bed'].get('bed15name')
            self.Bed15=QLabel(value2,self)
            self.Bed15.setFont(lb_font)
            self.Bed15.resize(200, 95)
            self.Bed15.move(590,380)
        if(self.total_bed>15):
            value2 = config['Total_Bed'].get('bed16name')
            self.Bed16=QLabel(value2,self)
            self.Bed16.setFont(lb_font)
            self.Bed16.resize(200, 95)
            self.Bed16.move(795,380)
        if(self.total_bed>16):
            value2 = config['Total_Bed'].get('bed17name')
            self.Bed17=QLabel(value2,self)
            self.Bed17.setFont(lb_font)
            self.Bed17.resize(200, 95)
            self.Bed17.move(1000,380)
        if(self.total_bed>17):
            value2 = config['Total_Bed'].get('bed18name')
            self.Bed18=QLabel(value2,self)
            self.Bed18.setFont(lb_font)
            self.Bed18.resize(200, 95)
            self.Bed18.move(1205,380)
        
        if(self.total_bed>18):
            value2 = config['Total_Bed'].get('bed19name')
            self.Bed19=QLabel(value2,self)
            self.Bed19.setFont(lb_font)
            self.Bed19.resize(200, 95)
            self.Bed19.move(180,480)
        if(self.total_bed>19):
            value2 = config['Total_Bed'].get('bed20name')
            self.Bed20=QLabel(value2,self)
            self.Bed20.setFont(lb_font)
            self.Bed20.resize(200, 95)
            self.Bed20.move(385,480)
        if(self.total_bed>20):
            value2 = config['Total_Bed'].get('bed21name')
            self.Bed21=QLabel(value2,self)
            self.Bed21.setFont(lb_font)
            self.Bed21.resize(200, 95)
            self.Bed21.move(590,480)
        if(self.total_bed>21):
            value2 = config['Total_Bed'].get('bed22name')
            self.Bed22=QLabel(value2,self)
            self.Bed22.setFont(lb_font)
            self.Bed22.resize(200, 95)
            self.Bed22.move(795,480)
        if(self.total_bed>22):
            value2 = config['Total_Bed'].get('bed23name')
            self.Bed23=QLabel(value2,self)  
            self.Bed23.setFont(lb_font)
            self.Bed23.resize(200, 95)
            self.Bed23.move(1000,480)
        if(self.total_bed>23):
            value2 = config['Total_Bed'].get('bed24name')
            self.Bed24=QLabel(value2,self)
            self.Bed24.resize(200, 95)
            self.Bed24.setFont(lb_font)
            self.Bed24.move(1205,480)
        if(self.total_bed>24):
            value2 = config['Total_Bed'].get('bed25name')
            self.Bed25=QLabel(value2,self)
            self.Bed25.setFont(lb_font)
            self.Bed25.resize(200, 95)
            self.Bed25.move(180,580)
        if(self.total_bed>25):
            value2 = config['Total_Bed'].get('bed26name')
            self.Bed26=QLabel(value2,self)
            self.Bed26.setFont(lb_font)
            self.Bed26.resize(200, 95)
            self.Bed26.move(385,580)
        if(self.total_bed>26):
            value2 = config['Total_Bed'].get('bed27name')
            self.Bed27=QLabel(value2,self)
            self.Bed27.setFont(lb_font)
            self.Bed27.resize(200, 95)
            self.Bed27.move(590,580)
        if(self.total_bed>27):
            value2 = config['Total_Bed'].get('bed28name')
            self.Bed28=QLabel(value2,self)
            self.Bed28.setFont(lb_font)
            self.Bed28.resize(200, 95)
            self.Bed28.move(795,580)
        if(self.total_bed>28):
            value2 = config['Total_Bed'].get('bed29name')
            self.Bed29=QLabel(value2,self)
            self.Bed29.setFont(lb_font)
            self.Bed29.resize(200, 95)
            self.Bed29.move(1000,580)
        if(self.total_bed>29):
            value2 = config['Total_Bed'].get('bed30name')
            self.Bed30=QLabel(value2,self)
            self.Bed30.setFont(lb_font)
            self.Bed30.resize(200, 95)
            self.Bed30.move(1205,580)
        
        if(self.total_bed>30):
            value2 = config['Total_Bed'].get('bed31name')
            self.Bed31=QLabel(value2,self)
            self.Bed31.setFont(lb_font)
            self.Bed31.resize(200, 95)
            self.Bed31.move(180,680)
        if(self.total_bed>31):
            value2 = config['Total_Bed'].get('bed32name')
            self.Bed32=QLabel(value2,self)   
            self.Bed32.setFont(lb_font)
            self.Bed32.resize(200, 95)
            self.Bed32.move(385,680)
        
        self.Bed33=QLabel("",self)   
        self.Bed33.setFont(lb_font)
        self.Bed33.resize(200, 95)
        self.Bed33.move(590,680)
        self.Bed33.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
        
        self.Bed34=QLabel("",self)   
        self.Bed34.setFont(lb_font)
        self.Bed34.resize(200, 95)
        self.Bed34.move(795,680)
        self.Bed34.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
        
        self.Bed35=QLabel("",self)   
        self.Bed35.setFont(lb_font)
        self.Bed35.resize(200, 95)
        self.Bed35.move(1000,680)
        self.Bed35.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
        
        self.Bed36=QLabel("",self)   
        self.Bed36.setFont(lb_font)
        self.Bed36.resize(200, 95)
        self.Bed36.move(1205,680)
        self.Bed36.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
        
        #self.Bed01.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
        
        
        self.timelabel = QLabel(self)
        self.timelabel.move(800,700)
        self.timelabel.setStyleSheet("* {color: white;background: qlineargradient( x1:0 y1:0, x2:0 y2:1, stop:0 rgb(84, 158, 151), stop:1 rgb(10, 33, 31));}")
        self.timelabel.hide()
           
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update_label)
        self.timer.start()
        #room_no[]={"0001","0002","0003
        
        self.clocklabel1=QLabel(": Time :",self)
        self.clocklabel1.setAlignment(Qt.AlignCenter)
        self.clocklabel1.resize(140,32)
        self.clocklabel1.setFont(QFont('Times', 20))
        self.clocklabel1.setStyleSheet("font-weight: bold;")
        self.clocklabel1.move(5,470)
        #self.clocklabel1.setText("Time:")
        
        self.clocklabel2=QLabel("001",self)
        self.clocklabel2.setAlignment(Qt.AlignCenter)
        self.clocklabel2.resize(140,32)
        self.clocklabel2.setFont(QFont('DS-Digital', 25))
        self.clocklabel2.setStyleSheet("font-weight: bold; color: #008000")
        self.clocklabel2.move(5,505)
        
        self.Datelabel1=QLabel(": Date :",self)
        self.Datelabel1.setAlignment(Qt.AlignCenter)
        self.Datelabel1.resize(140,32)
        self.Datelabel1.setFont(QFont('Times', 20))
        self.Datelabel1.setStyleSheet("font-weight: bold;")
        self.Datelabel1.move(5,380)
        #self.clocklabel1.setText("Time:")
        
        self.Datelabel2=QLabel("01/01/2021",self)
        self.Datelabel2.setAlignment(Qt.AlignCenter)
        self.Datelabel2.resize(140,32)
        self.Datelabel2.setFont(QFont('DS-Digital', 25))
        self.Datelabel2.setStyleSheet("font-weight: bold; color: #008000")
        self.Datelabel2.move(5,415)
        
        
        self.piclabel=QLabel("",self)
        #self.piclabel.setScaledContents(True)
        
        #self.clocklabel2.setAlignment(Qt.AlignRight)
        #self.clocklabel2.setFont(QFont('Arial', 20))
        self.piclabel.resize(240,120)
        self.piclabel.move(5,10)
        self.image = QImage("./LOGONO.PNG")
        #self.image = QImage("./Omni.png")
        
        
        self.imagepix = QPixmap.fromImage(self.image)
        self.piclabel.setScaledContents(True)
        self.piclabel.setPixmap(self.imagepix)
        self.piclabel.hide()
        
        #self.piclabel.resize(450,200)
        #self.pixmap = QPixmap("./Softechlogo.jpg")      
        #-self.pixmap = QPixmap("./LOGONO.PNG")
        #-self.piclabel.setPixmap(self.pixmap)
        
        self.piclabel=QLabel("",self) #logo hospital
        #self.clocklabel2.setAlignment(Qt.AlignRight)
        #self.clocklabel2.setFont(QFont('Arial', 20))
        self.piclabel.resize(240,120)
        self.piclabel.move(40,15)
        #self.piclabel.resize(450,200)
        #self.pixmap = QPixmap("./Softechlogo.jpg")
        #self.image = QImage("./LOGONO.PNG")
        self.image = QImage("./Omni.png")
        self.imagepix = QPixmap.fromImage(self.image)
        self.piclabel.setScaledContents(True)
        self.piclabel.setPixmap(self.imagepix)
        #self.piclabel.setPixmap(self.pixmap)
        
        self.piclabel1=QLabel("",self)
        self.piclabel1.resize(85,80)
        self.piclabel1.move(670,40)
        self.image_pic = QImage("./nurse.png")
        self.imagepix_pic = QPixmap.fromImage(self.image_pic)
        self.piclabel1.setScaledContents(True)
        self.piclabel1.setPixmap(self.imagepix_pic)
        
        self.hsptl_log=QLabel("",self)
        self.hsptl_log.resize(150,150)
        self.hsptl_log.move(1250,10)
        self.image_log = QImage("./AIIMS DEOGHAR.jpeg")
        self.imagepix_log = QPixmap.fromImage(self.image_log)
        self.hsptl_log.setScaledContents(True)
        self.hsptl_log.setPixmap(self.imagepix_log)
        
        self.stationlabel1=QLabel("Nurse Station",self)
        font = QFont()
        font.setPointSize(35)
        #font.setItalic(True)
        font.setUnderline(True)
        font.setWeight(100)
        self.stationlabel1.setAlignment(Qt.AlignCenter)
        self.stationlabel1.resize(300,50)
        self.stationlabel1.setFont(font)#QFont('Arial', 30,QFont.Bold))
        #self.stationlabel1.setFontItalic(True)
         
        self.stationlabel1.setStyleSheet("color: #357EC7")
        self.stationlabel1.move(570,110)
        ###################################################
        self.received_textedit=QPlainTextEdit("",self)
        self.received_textedit.resize(120,30)
        #self.received_textedit.insertPlainText("")
        self.received_textedit.move(15,830)
        self.received_textedit.setFont(QFont('Times', 6))
        self.received_textedit.setReadOnly(True)
        
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(Qt.black)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        painter.drawLine(0,170,1440,170)
        painter.drawLine(0,175,1440,175)
        painter.drawLine(150,175,150,900)
        painter.drawLine(155,175,155,900)
    @property
    def port(self) -> str:
        """Return the current serial port."""
        return self.port_combobox.currentData()
    def mid(s, offset, amount):
        return s[offset:offset+amount]
    def closeEvent(self, event: QCloseEvent) -> None:
        """Handle Close event of the Widget."""
        if ser.is_open:
            ser.close()

        #self._save_settings()  #for save settings

        event.accept()

    def on_connect_btn_pressed(self) -> None:
        """Open serial connection to the specified port."""
        if ser.is_open:
            ser.close()
        ser.port = self.port
        ser.baudrate = SER_BAUDRATE
        
        try:
            ser.open()
        except Exception as e:
            self.show_error_message(str(e))

        if ser.is_open:
            self.connect_btn.setVisible(False)
            self.disconnect_btn.setVisible(True)
            self.port_combobox.setDisabled(True)
            self.msg_lineedit.setEnabled(True)
            self.send_btn.setEnabled(True)
            loop.create_task(self.receive_serial_async())

    def on_disconnect_btn_pressed(self) -> None:
        """Close current serial connection."""
        if ser.is_open:
            ser.close()

        if not ser.is_open:
            self.connect_btn.setVisible(True)
            self.disconnect_btn.setVisible(False)
            self.port_combobox.setEnabled(True)
            self.msg_lineedit.setEnabled(False)
            self.send_btn.setEnabled(False)

    def on_send_btn_pressed(self) -> None:
        """Send message to serial port."""
        msg = self.msg_lineedit.text() + '\r\n'
        loop.call_soon(send_serial_async, msg)

    async def receive_serial_async(self) -> None:
        """Wait for incoming data, convert it to text and add to Textedit."""
        while True:
            try:
                msg = ser.read()
                if msg != b'':
                    text = msg.decode()#.strip()
                    #print(text)
                    
                    if text=="$":
                        text="$"
                    if text=="\r":
                        
                        if self.text1!=0:
                            #comm light gui
                            self.lb_msg.hide()
                        print("lenght : ",len(self.text1))
                        if len(self.text1)==7:
                            
                            if self.text1[0:1]=="$":
                                #print(len(text))
                                self.ID=  self.text1[1:3]
                                self.flag_arr[int(self.ID)]=self.text1[1:3] 
                                           
                                text2 = self.text1[3:len(self.text1)]
                                print("text :"+text2)
                                
                                index = 1
                                for value in text2:
                                    #print("Value : ",index, value)
                                    temp = self.config1[self.ID].get("pos" + str(index))
                                    self.flag_arr[int(self.ID)]=self.flag_arr[int(self.ID)] + "," + str(value)
                                   
                                    for k in range(1,33):
                                        #self.received_textedit.appendPlainText(str(k))#self.array_str[k]
                                        #print(self.status_arr)
                                        
                                        if str(self.array_str[k])==str(temp):
                                            #self.stat=d self.text1[3:2]
                                            self.status_arr[k] = str(value)
                                            self.received_textedit.appendPlainText(str(temp)+ " P " +value)#self.status_arr.append
                                    index += 1
                                self.flag_arr[int(self.ID)]=self.flag_arr[int(self.ID)]+"*"
                                #print(self.flag_arr[int(self.ID)])
                                
                             
                            
                        self.text1=""
                    else:
                        self.text1=self.text1 + str(text)
                await asyncio.sleep(0)    
            except:
                 pass
            
    
    def update_com_ports(self) -> None:
        #Update COM Port list in GUI.
        for name, device in gen_serial_ports():
            self.port_combobox.addItem(name, device)    
    
    def update_label(self) -> None:
        #Update COM Port list in GUI.
        #global timeval
       
            
        
        self.timeval=self.timeval+1     
        self.timelabel.setText(str(self.timeval))
        self.clocklabel2.setText(QtCore.QDateTime.currentDateTime().toString("hh:mm:ss"))
        self.Datelabel2.setText(QtCore.QDateTime.currentDateTime().toString("dd/MM/yy"))
        
        if self.comm_blink==1:
            GPIO.output(self.comnunication, GPIO.LOW)
            print("comm light off")
            self.comm_blink=0
        else:
            GPIO.output(self.comnunication, GPIO.HIGH)
            print("comm light on")
            self.comm_blink=1
            
        
        self.input_state = GPIO.input(self.switch)
        if self.input_state == False:
            print('Button Pressed1')
            GPIO.output(self.buzzer, GPIO.LOW)
            if self.buzzer_flag==1:
                self.btn_press=1
                self.switch_count=0
                vol3 = self.m.setvolume(0) ##volume down
                self.lb_Mute.setText("Mute ON")
                self.lb_Mute.setStyleSheet("color: white; font-size:20px; qproperty-alignment: AlignCenter; font-weight: bold; Background-color: Red; border-radius: 10px;")
        
                
            
        if self.btn_press==1:
            self.buzzer_flag=0
            self.switch_count=self.switch_count+self.btn_press
            print("Counter : "+str(self.switch_count))
            if self.switch_count>=60:
                self.buzzer_flag=1
                self.btn_press=0
                vol4 = self.m.setvolume(100) ##volume up
                self.lb_Mute.setText("Mute Off")
                self.lb_Mute.setStyleSheet("color: white; font-size:20px; qproperty-alignment: AlignCenter; font-weight: bold; Background-color: Green; border-radius: 10px;")
        
        
        
        if self.buzzer_flag==2:
            if self.em_blink==1:
                GPIO.output(self.buzzer,GPIO.LOW)
                print("blink")
                self.em_blink=0 
            else:
                GPIO.output(self.buzzer,GPIO.HIGH)
                print("not blink")
                self.em_blink=1
                
        elif self.buzzer_flag==1:
            self.countLoop=self.countLoop+1
            if self.countLoop>=2:
                self.countLoop=0
                if self.nor_blink==1:
                    GPIO.output(self.buzzer,GPIO.LOW)
                    print("blink")
                    self.nor_blink=0
                else:
                    GPIO.output(self.buzzer,GPIO.HIGH)
                    print("not blink")
                    self.nor_blink=1
                    
        index=1
        index2=1
        index3=1
        offflag=0
        for j in range(1, 33):
            
            if self.status_arr[j]=="1":
                if self.buzzer_flag!=2:
                    self.buzzer_flag=1
                    offflag=1
            if self.status_arr[j]=="2":
                self.buzzer_flag=2
                offflag=1
                
            
            #write code blue in my.ini file       
            if self.status_arr[j]=="3":
                vol4 = self.m.setvolume(100) ##volume up
                code_bed = self.config1.get("Total_Bed", "bed"+str(j)+"name")
                room= "Room_no_"+str(index)
                #print("print "+room,index,code_bed)
                self.config2.set("Code_Blue", room, code_bed)
                with open("/home/pi/Share_Folder/my.ini", 'w') as configfile:
                    self.config2.write(configfile)
                index=index+1
                if index==6:
                    index=1
            #to read my.ini file write normal code blue         
            if self.status_arr[j]=="0":
                code_bed = self.config1.get("Total_Bed", "bed"+str(j)+"name")
                
                string_val1 =  self.config2.get("Code_Blue", "Room_no_1")
                string_val2 =  self.config2.get("Code_Blue", "Room_no_2")
                string_val3 =  self.config2.get("Code_Blue", "Room_no_3")
                string_val4 =  self.config2.get("Code_Blue", "Room_no_4")
                string_val5 =  self.config2.get("Code_Blue", "Room_no_5")
                
                if string_val1==code_bed:
                    self.label_c_blue.setText("")
                    print(string_val1, code_bed)
                    self.config2.set("Code_Blue", "Room_no_1", "")
                    with open("/home/pi/Share_Folder/my.ini", 'w') as configfile:
                        self.config2.write(configfile)

                if string_val2==code_bed:
                    self.label_c_blue.setText("")
                    print(string_val2, code_bed)
                    self.config2.set("Code_Blue", "Room_no_2", "")
                    with open("/home/pi/Share_Folder/my.ini", 'w') as configfile:
                        self.config2.write(configfile)
                        
                if string_val3==code_bed:
                    self.label_c_blue.setText("")
                    print(string_val3, code_bed)
                    self.config2.set("Code_Blue", "Room_no_3", "")
                    with open("/home/pi/Share_Folder/my.ini", 'w') as configfile:
                        self.config2.write(configfile)
                        
                if string_val4==code_bed:
                    self.label_c_blue.setText("")
                    print(string_val4, code_bed)
                    self.config2.set("Code_Blue", "Room_no_4", "")
                    with open("/home/pi/Share_Folder/my.ini", 'w') as configfile:
                        self.config2.write(configfile)
                        
                if string_val5==code_bed:
                    self.label_c_blue.setText("")
                    print(string_val5, code_bed)
                    self.config2.set("Code_Blue", "Room_no_5", "")
                    with open("/home/pi/Share_Folder/my.ini", 'w') as configfile:
                        self.config2.write(configfile)
                        
            #write code Emergency in my.ini file    
            if self.status_arr[j]=="2":
                vol4 = self.m.setvolume(100) ##volume up
                code_bed = self.config1.get("Total_Bed", "bed"+str(j)+"name")
                room= "Room_no_"+str(index2)
                print(room,index2,code_bed)
                self.config2.set("Code_Emergency", room, code_bed)
                with open("/home/pi/Share_Folder/my.ini", 'w') as configfile:
                    self.config2.write(configfile)
                index2=index2+1
                if index2==6:
                    index2=1
            
            #to read my.ini file write normal code Emergency        
            if self.status_arr[j]=="0":
                code_bed = self.config1.get("Total_Bed", "bed"+str(j)+"name")
                
                string_val1 =  self.config2.get("Code_Emergency", "Room_no_1")
                string_val2 =  self.config2.get("Code_Emergency", "Room_no_2")
                string_val3 =  self.config2.get("Code_Emergency", "Room_no_3")
                string_val4 =  self.config2.get("Code_Emergency", "Room_no_4")
                string_val5 =  self.config2.get("Code_Emergency", "Room_no_5")
                
                if string_val1==code_bed:
                    print(string_val1, code_bed)
                    self.config2.set("Code_Emergency", "Room_no_1", "")
                    with open("/home/pi/Share_Folder/my.ini", 'w') as configfile:
                        self.config2.write(configfile)

                if string_val2==code_bed:
                    print(string_val2, code_bed)
                    self.config2.set("Code_Emergency", "Room_no_2", "")
                    with open("/home/pi/Share_Folder/my.ini", 'w') as configfile:
                        self.config2.write(configfile)
                        
                if string_val3==code_bed:
                    print(string_val3, code_bed)
                    self.config2.set("Code_Emergency", "Room_no_3", "")
                    with open("/home/pi/Share_Folder/my.ini", 'w') as configfile:
                        self.config2.write(configfile)
                        
                if string_val4==code_bed:
                    print(string_val4, code_bed)
                    self.config2.set("Code_Emergency", "Room_no_4", "")
                    with open("/home/pi/Share_Folder/my.ini", 'w') as configfile:
                        self.config2.write(configfile)
                        
                if string_val5==code_bed:
                    print(string_val5, code_bed)
                    self.config2.set("Code_Emergency", "Room_no_5", "")
                    with open("/home/pi/Share_Folder/my.ini", 'w') as configfile:
                        self.config2.write(configfile)
                        
                        
            #write code Normal in my.ini file    
            if self.status_arr[j]=="1":
                code_bed = self.config1.get("Total_Bed", "bed"+str(j)+"name")
                room= "Room_no_"+str(index3)
                print(room,index3,code_bed)
                self.config2.set("Code_Normal", room, code_bed)
                with open("/home/pi/Share_Folder/my.ini", 'w') as configfile:
                    self.config2.write(configfile)
                index3=index3+1
                if index3==6:
                    index3=1
            
            #to read my.ini file write normal code Normal        
            if self.status_arr[j]=="0":
                code_bed = self.config1.get("Total_Bed", "bed"+str(j)+"name")
                
                string_val1 =  self.config2.get("Code_Normal", "Room_no_1")
                string_val2 =  self.config2.get("Code_Normal", "Room_no_2")
                string_val3 =  self.config2.get("Code_Normal", "Room_no_3")
                string_val4 =  self.config2.get("Code_Normal", "Room_no_4")
                string_val5 =  self.config2.get("Code_Normal", "Room_no_5")
                
                if string_val1==code_bed:
                    print(string_val1, code_bed)
                    self.config2.set("Code_Normal", "Room_no_1", "")
                    with open("/home/pi/Share_Folder/my.ini", 'w') as configfile:
                        self.config2.write(configfile)

                if string_val2==code_bed:
                    print(string_val2, code_bed)
                    self.config2.set("Code_Normal", "Room_no_2", "")
                    with open("/home/pi/Share_Folder/my.ini", 'w') as configfile:
                        self.config2.write(configfile)
                        
                if string_val3==code_bed:
                    print(string_val3, code_bed)
                    self.config2.set("Code_Normal", "Room_no_3", "")
                    with open("/home/pi/Share_Folder/my.ini", 'w') as configfile:
                        self.config2.write(configfile)
                        
                if string_val4==code_bed:
                    print(string_val4, code_bed)
                    self.config2.set("Code_Normal", "Room_no_4", "")
                    with open("/home/pi/Share_Folder/my.ini", 'w') as configfile:
                        self.config2.write(configfile)
                        
                if string_val5==code_bed:
                    print(string_val5, code_bed)
                    self.config2.set("Code_Normal", "Room_no_5", "")
                    with open("/home/pi/Share_Folder/my.ini", 'w') as configfile:
                        self.config2.write(configfile)
                 
            
        config3 = ConfigParser()
        config3.read("/home/pi/Share_Folder/my.ini")
        Code_room1=config3['Code_Blue'].get('Room_no_1')
        Code_room2=config3['Code_Blue'].get('Room_no_2')
        Code_room3=config3['Code_Blue'].get('Room_no_3')
        Code_room4=config3['Code_Blue'].get('Room_no_4')
        Code_room5=config3['Code_Blue'].get('Room_no_5')
        list7 = []
        
        list7 = [Code_room1, Code_room2, Code_room3, Code_room4, Code_room5]
        value12= '   '.join([str(elem) for elem in list7])
        #print(len(value12))
        
        if len(value12)==12:
            self.label_c_blue.setText("AIIMS DEOGHAR")
        else:
            self.label_c_blue.setText("Code Blue "+value12)
        
        
              
              
              
        if offflag==0:
           self.buzzer_flag=0
        
        directory= str(QtCore.QDateTime.currentDateTime().toString("ddMMyy"))
        parent_dir = "/home/pi/Share_Folder/"
        path= str(parent_dir +"/" + directory+"/")
        if os.path.isdir(path):
            for j in range(1, 33):
                if self.flag_arr[j]!="0":
                    Id_dir = self.flag_arr[int(self.ID)][0:2]
                    
                    #print("flag vlaue :",self.flag_arr[j])
                    
                    id_parent_dir2 = "/home/pi/Share_Folder/"+ directory +"/"
                    id_path= str(id_parent_dir2 + Id_dir  +"/")
                    if os.path.isdir(id_path):
                        file = str(QtCore.QDateTime.currentDateTime().toString("ddMMyy"))+" "+str(Id_dir)+".csv"
                        cdate= str(QtCore.QDateTime.currentDateTime().toString("ddMMyy"))
                        ctime= str(QtCore.QDateTime.currentDateTime().toString("hhmmss"))
                        if os.path.exists(id_path+file):
                            print(os.path.exists(id_path+file))
                            
                            if self.flag_arr[int(self.ID)][0:2]!="0":
                                
                                dupstr=self.flag_arr[int(self.ID)].replace('*', '')
                                dupstr = cdate+","+ ctime +","+ dupstr  
                                #print(dupstr)
                                List=dupstr.split(',')
                                #print(List)
                                list2=list(map(int,List))
                                #print(list2)
                                
                                with open(id_path+file, 'a') as f_object:
                                    self.writer_object = writer(f_object)
                                    self.writer_object.writerow(list2)
                                    f_object.close()
                                    
                                list2=""
                                      
                                            
                        else:
                            #.csv file create if not exists
                            #open(os.path.join(id_path, file), 'wb')
                            
                            with open(id_path+file, 'w', newline='') as outcsv:
                                self.writer = csv.DictWriter(outcsv, fieldnames = ["Date", "Time", "ID", "Pos1", "Pos2", "Pos3", "Pos4", "Pos5", "Pos6", "Pos7", "Pos8", "Pos10", "Pos11", "Pos12", "Pos13", "Pos14", "Pos15", "Pos16", "Pos17", "Pos18", "Pos19", "Pos20"])
                                self.writer.writeheader()
                            
                        
                            
                    else:
                        id_path2 = os.path.join(id_parent_dir2, Id_dir) 
                        os.mkdir(id_path2)
                        #print("Directory '% s' created" % Id_dir)
                    
                
            
            #print(self.ID)
        else:
            path2 = os.path.join(parent_dir, directory) 
            os.mkdir(path2) 
            #print("Directory '% s' created" % directory)
        
        if ser.is_open:
            if self.count<10:
                msg = "$0"+ str(self.count) + '\r\n'
            else:
                msg = "$"+ str(self.count) + '\r\n' 
            loop.call_soon(send_serial_async, msg)
            
            if self.count < int(self.controller_max_id):
                self.count += 1
                #self.lb_msg.setText("Send")
                self.lb_msg.show()
            else:
                self.count =1
                
            #for j in range(1, 33):
             #   if self.flag_arr[j]!=0:
              #      print(self.flag_arr[j])
            
            #print(self.total_bed)
            if self.blink==0:
                self.count_blinker=self.count_blinker+1       
                if self.count_blinker==2:
                    self.count_blinker=0
                    self.blink=1
                for j in range(1, 33):
                    if(self.total_bed>0):
                        if self.status_arr[1]=="0":
                            self.Bed01.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                        self.value2 = self.config1['Total_Bed'].get('bed1name')
                        self.Bed01.setText(self.value2)
                        
                    if(self.total_bed>1):
                        if self.status_arr[2]=="0":
                            self.Bed02.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                        self.value2 = self.config1['Total_Bed'].get('bed2name')
                        self.Bed02.setText(self.value2)
                    
                    if(self.total_bed>2):
                        if self.status_arr[3]=="0":
                            self.Bed03.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                        self.value2 = self.config1['Total_Bed'].get('bed3name')
                        self.Bed03.setText(self.value2)
                    
                    if(self.total_bed>3):
                        if self.status_arr[4]=="0":
                            self.Bed04.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                        self.value2 = self.config1['Total_Bed'].get('bed4name')
                        self.Bed04.setText(self.value2)
                        
                    if(self.total_bed>4):
                        if self.status_arr[5]=="0":
                            self.Bed05.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                        self.value2 = self.config1['Total_Bed'].get('bed5name')
                        self.Bed05.setText(self.value2)
                        
                    if(self.total_bed>5):
                        if self.status_arr[6]=="0":
                            self.Bed06.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                        self.value2 = self.config1['Total_Bed'].get('bed6name')
                        self.Bed06.setText(self.value2)
                    
                    if(self.total_bed>6):
                        if self.status_arr[7]=="0":
                            self.Bed07.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                        self.value2 = self.config1['Total_Bed'].get('bed7name')
                        self.Bed07.setText(self.value2)
                    
                    if(self.total_bed>7):
                        if self.status_arr[8]=="0":
                            self.Bed08.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                        self.value2 = self.config1['Total_Bed'].get('bed8name')
                        self.Bed08.setText(self.value2)
                        
                    if(self.total_bed>8):
                        if self.status_arr[9]=="0":
                            self.Bed09.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                        self.value2 = self.config1['Total_Bed'].get('bed9name')
                        self.Bed09.setText(self.value2)
                        
                    if(self.total_bed>9):
                        if self.status_arr[10]=="0":
                            self.Bed10.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                        self.value2 = self.config1['Total_Bed'].get('bed10name')
                        self.Bed10.setText(self.value2)
                        
                    if(self.total_bed>10):
                        if self.status_arr[11]=="0":
                            self.Bed11.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                        self.value2 = self.config1['Total_Bed'].get('bed11name')
                        self.Bed11.setText(self.value2)
                        
                    if(self.total_bed>11):
                        if self.status_arr[12]=="0":
                            self.Bed12.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                        self.value2 = self.config1['Total_Bed'].get('bed12name')
                        self.Bed12.setText(self.value2)
                    
                    if(self.total_bed>12):
                        if self.status_arr[13]=="0":
                            self.Bed13.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                        self.value2 = self.config1['Total_Bed'].get('bed13name')
                        self.Bed13.setText(self.value2)
                    
                    if(self.total_bed>13):
                        if self.status_arr[14]=="0":
                            self.Bed14.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                        self.value2 = self.config1['Total_Bed'].get('bed14name')
                        self.Bed14.setText(self.value2)
                        
                    if(self.total_bed>14):
                        if self.status_arr[15]=="0":
                            self.Bed15.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                        self.value2 = self.config1['Total_Bed'].get('bed15name')
                        self.Bed15.setText(self.value2)
                        
                    if(self.total_bed>15):
                        if self.status_arr[16]=="0":
                            self.Bed16.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                        self.value2 = self.config1['Total_Bed'].get('bed16name')
                        self.Bed16.setText(self.value2)
                    if(self.total_bed>16):
                        if self.status_arr[17]=="0":
                            self.Bed17.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                        self.value2 = self.config1['Total_Bed'].get('bed17name')
                        self.Bed17.setText(self.value2)
                        
                    if(self.total_bed>17):
                        if self.status_arr[18]=="0":
                            self.Bed18.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                        self.value2 = self.config1['Total_Bed'].get('bed18name')
                        self.Bed18.setText(self.value2)
                        
                    if(self.total_bed>18):
                        if self.status_arr[19]=="0":
                            self.Bed19.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                        self.value2 = self.config1['Total_Bed'].get('bed19name')
                        self.Bed19.setText(self.value2)
                    
                    if(self.total_bed>19):
                        if self.status_arr[20]=="0":
                            self.Bed20.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                        self.value2 = self.config1['Total_Bed'].get('bed20name')
                        self.Bed20.setText(self.value2)
                    
                    if(self.total_bed>20):
                        if self.status_arr[21]=="0":
                            self.Bed21.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                        self.value2 = self.config1['Total_Bed'].get('bed21name')
                        self.Bed21.setText(self.value2)
                    
                    if(self.total_bed>21):
                        if self.status_arr[22]=="0":
                            self.Bed22.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                        self.value2 = self.config1['Total_Bed'].get('bed22name')
                        self.Bed22.setText(self.value2)
                    if(self.total_bed>22):
                        if self.status_arr[23]=="0":
                            self.Bed23.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                        self.value2 = self.config1['Total_Bed'].get('bed23name')
                        self.Bed23.setText(self.value2)
                        
                    if(self.total_bed>23):
                        if self.status_arr[24]=="0":
                            self.Bed24.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                        self.value2 = self.config1['Total_Bed'].get('bed24name')
                        self.Bed24.setText(self.value2)
                        
                    if(self.total_bed>24):
                        if self.status_arr[25]=="0":
                            self.Bed25.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                        self.value2 = self.config1['Total_Bed'].get('bed25name')
                        self.Bed25.setText(self.value2)
                        
                    if(self.total_bed>25):
                        if self.status_arr[26]=="0":
                            self.Bed26.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                        self.value2 = self.config1['Total_Bed'].get('bed26name')
                        self.Bed26.setText(self.value2)
                        
                    if(self.total_bed>26):
                        if self.status_arr[27]=="0":
                            self.Bed27.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                        self.value2 = self.config1['Total_Bed'].get('bed27name')
                        self.Bed27.setText(self.value2)
                        
                    if(self.total_bed>27):
                        if self.status_arr[28]=="0":
                            self.Bed28.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                        self.value2 = self.config1['Total_Bed'].get('bed28name')
                        self.Bed28.setText(self.value2)
                        
                    if(self.total_bed>28):
                        if self.status_arr[29]=="0":
                            self.Bed29.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                        self.value2 = self.config1['Total_Bed'].get('bed29name')
                        self.Bed29.setText(self.value2)
                        
                    if(self.total_bed>29):
                        if self.status_arr[30]=="0":
                            self.Bed30.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                        self.value2 = self.config1['Total_Bed'].get('bed30name')
                        self.Bed30.setText(self.value2)
                        
                    if(self.total_bed>30):
                        if self.status_arr[31]=="0":
                            self.Bed31.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                        self.value2 = self.config1['Total_Bed'].get('bed31name')
                        self.Bed31.setText(self.value2)
                        
                    if(self.total_bed>31):
                        if self.status_arr[32]=="0":
                            self.Bed32.setStyleSheet("background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                        self.value2 = self.config1['Total_Bed'].get('bed32name')
                        self.Bed32.setText(self.value2)
                        if self.status_arr[j]=="0":
                           if len(value12)==12:
                               self.label_c_blue.setText("AIIMS DEOGHAR")
                           else:
                               self.label_c_blue.setText("Code Blue "+value12)
                           
                    
            else:
                for j in range(1, 33):
                   if self.status_arr[j]=="3":
                      if len(value12)==12:
                          self.label_c_blue.setText("AIIMS DEOGHAR")
                      else:
                          self.label_c_blue.setText("")
                   if(self.total_bed>0):
                        if self.status_arr[1]=="1":
                            self.Bed01.setText("")
                   if(self.total_bed>0):
                        if self.status_arr[1]=="2":
                            self.Bed01.setText("")
                            self.Bed01.setStyleSheet("color: Red; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   if(self.total_bed>0):
                        if self.status_arr[1]=="3":
                            self.Bed01.setText("")
                            self.Bed01.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                            
                   if(self.total_bed>1):
                        if self.status_arr[2]=="1":
                            self.Bed02.setText("")
                   if(self.total_bed>1):
                        if self.status_arr[2]=="2":
                            self.Bed02.setText("")
                            self.Bed02.setStyleSheet("color: Red; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   if(self.total_bed>1):
                        if self.status_arr[2]=="3":
                            self.Bed02.setText("")
                            self.Bed02.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")         
                   
                   if(self.total_bed>2):
                        if self.status_arr[3]=="1":
                            self.Bed03.setText("")
                   if(self.total_bed>2):
                        if self.status_arr[3]=="2":
                            self.Bed03.setText("")
                            self.Bed03.setStyleSheet("color: Red; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   if(self.total_bed>2):
                        if self.status_arr[3]=="3":
                            self.Bed03.setText("")
                            self.Bed03.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                            
                   if(self.total_bed>3):
                        if self.status_arr[4]=="1":
                            self.Bed04.setText("")
                   if(self.total_bed>3):
                        if self.status_arr[4]=="2":
                            self.Bed04.setText("")
                            self.Bed04.setStyleSheet("color: Red; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   if(self.total_bed>3):
                        if self.status_arr[4]=="3":
                            self.Bed04.setText("")
                            self.Bed04.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   
                   if(self.total_bed>4):
                        if self.status_arr[5]=="1":
                            self.Bed05.setText("")
                   if(self.total_bed>4):
                        if self.status_arr[5]=="2":
                            self.Bed05.setText("")
                            self.Bed05.setStyleSheet("color: Red; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   if(self.total_bed>4):
                        if self.status_arr[5]=="3":
                            self.Bed05.setText("")
                            self.Bed05.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                            
                   if(self.total_bed>5):
                        if self.status_arr[6]=="1":
                            self.Bed06.setText("")
                   if(self.total_bed>5):
                        if self.status_arr[6]=="2":
                            self.Bed06.setText("")
                            self.Bed06.setStyleSheet("color: Red; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   if(self.total_bed>5):
                        if self.status_arr[6]=="3":
                            self.Bed06.setText("")
                            self.Bed06.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                            
                   if(self.total_bed>6):
                        if self.status_arr[7]=="1":
                            self.Bed07.setText("")
                   if(self.total_bed>6):
                        if self.status_arr[7]=="2":
                            self.Bed07.setText("")
                            self.Bed07.setStyleSheet("color: Red; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   if(self.total_bed>6):
                        if self.status_arr[7]=="3":
                            self.Bed07.setText("")
                            self.Bed07.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   
                   if(self.total_bed>7):
                        if self.status_arr[8]=="1":
                            self.Bed08.setText("")
                   if(self.total_bed>7):
                        if self.status_arr[8]=="2":
                            self.Bed08.setText("")
                            self.Bed08.setStyleSheet("color: Red; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   if(self.total_bed>7):
                        if self.status_arr[8]=="3":
                            self.Bed08.setText("")
                            self.Bed08.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   
                   if(self.total_bed>8):
                        if self.status_arr[9]=="1":
                            self.Bed09.setText("")
                   if(self.total_bed>8):
                        if self.status_arr[9]=="2":
                            self.Bed09.setText("")
                            self.Bed09.setStyleSheet("color: Red; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   if(self.total_bed>8):
                        if self.status_arr[9]=="3":
                            self.Bed09.setText("")
                            self.Bed09.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                            
                   if(self.total_bed>9):
                        if self.status_arr[10]=="1":
                            self.Bed10.setText("")
                   if(self.total_bed>9):
                        if self.status_arr[10]=="2":
                            self.Bed10.setText("")
                            self.Bed10.setStyleSheet("color: Red; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   if(self.total_bed>9):
                        if self.status_arr[10]=="3":
                            self.Bed10.setText("")
                            self.Bed10.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   
                   if(self.total_bed>10):
                        if self.status_arr[11]=="1":
                            self.Bed11.setText("")
                   if(self.total_bed>10):
                        if self.status_arr[11]=="2":
                            self.Bed11.setText("")
                            self.Bed11.setStyleSheet("color: Red; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   if(self.total_bed>10):
                        if self.status_arr[11]=="3":
                            self.Bed11.setText("")
                            self.Bed11.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   
                   if(self.total_bed>11):
                        if self.status_arr[12]=="1":
                            self.Bed12.setText("")
                   if(self.total_bed>11):
                        if self.status_arr[12]=="2":
                            self.Bed12.setText("")
                            self.Bed12.setStyleSheet("color: Red; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   if(self.total_bed>11):
                        if self.status_arr[12]=="3":
                            self.Bed12.setText("")
                            self.Bed12.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   
                   if(self.total_bed>12):
                        if self.status_arr[13]=="1":
                            self.Bed13.setText("")
                   if(self.total_bed>12):
                        if self.status_arr[13]=="2":
                            self.Bed13.setText("")
                            self.Bed13.setStyleSheet("color: Red; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   if(self.total_bed>12):
                        if self.status_arr[13]=="3":
                            self.Bed13.setText("")
                            self.Bed13.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   
                   if(self.total_bed>13):
                        if self.status_arr[14]=="1":
                            self.Bed14.setText("")
                   if(self.total_bed>13):
                        if self.status_arr[14]=="2":
                            self.Bed14.setText("")
                            self.Bed14.setStyleSheet("color: Red; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   if(self.total_bed>13):
                        if self.status_arr[14]=="3":
                            self.Bed14.setText("")
                            self.Bed14.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                            
                   if(self.total_bed>14):
                        if self.status_arr[15]=="1":
                            self.Bed15.setText("")
                   if(self.total_bed>14):
                        if self.status_arr[15]=="2":
                            self.Bed15.setText("")
                            self.Bed15.setStyleSheet("color: Red; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   if(self.total_bed>14):
                        if self.status_arr[15]=="3":
                            self.Bed15.setText("")
                            self.Bed15.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   
                   if(self.total_bed>15):
                        if self.status_arr[16]=="1":
                            self.Bed16.setText("")
                   if(self.total_bed>15):
                        if self.status_arr[16]=="2":
                            self.Bed16.setText("")
                            self.Bed16.setStyleSheet("color: Red; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   if(self.total_bed>15):
                        if self.status_arr[16]=="3":
                            self.Bed16.setText("")
                            self.Bed16.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                            
                   if(self.total_bed>16):
                        if self.status_arr[17]=="1":
                            self.Bed17.setText("")
                   if(self.total_bed>16):
                        if self.status_arr[17]=="2":
                            self.Bed17.setText("")
                            self.Bed17.setStyleSheet("color: Red; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   if(self.total_bed>16):
                        if self.status_arr[17]=="3":
                            self.Bed17.setText("")
                            self.Bed17.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   
                   if(self.total_bed>17):
                        if self.status_arr[18]=="1":
                            self.Bed18.setText("")
                   if(self.total_bed>17):
                        if self.status_arr[18]=="2":
                            self.Bed18.setText("")
                            self.Bed18.setStyleSheet("color: Red; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   if(self.total_bed>17):
                        if self.status_arr[18]=="3":
                            self.Bed18.setText("")
                            self.Bed18.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   
                   if(self.total_bed>18):
                        if self.status_arr[19]=="1":
                            self.Bed19.setText("")
                   if(self.total_bed>18):
                        if self.status_arr[19]=="2":
                            self.Bed19.setText("")
                            self.Bed19.setStyleSheet("color: Red; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   if(self.total_bed>18):
                        if self.status_arr[19]=="3":
                            self.Bed19.setText("")
                            self.Bed19.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   
                   if(self.total_bed>19):
                        if self.status_arr[20]=="1":
                            self.Bed20.setText("")
                   if(self.total_bed>19):
                        if self.status_arr[20]=="2":
                            self.Bed20.setText("")
                            self.Bed20.setStyleSheet("color: Red; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   if(self.total_bed>19):
                        if self.status_arr[20]=="3":
                            self.Bed20.setText("")
                            self.Bed20.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   
                   if(self.total_bed>20):
                        if self.status_arr[21]=="1":
                            self.Bed21.setText("")
                   if(self.total_bed>20):
                        if self.status_arr[21]=="2":
                            self.Bed21.setText("")
                            self.Bed21.setStyleSheet("color: Red; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   if(self.total_bed>20):
                        if self.status_arr[21]=="3":
                            self.Bed21.setText("")
                            self.Bed21.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                            
                   if(self.total_bed>21):
                        if self.status_arr[22]=="1":
                            self.Bed22.setText("")
                   if(self.total_bed>21):
                        if self.status_arr[22]=="2":
                            self.Bed22.setText("")
                            self.Bed22.setStyleSheet("color: Red; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   if(self.total_bed>21):
                        if self.status_arr[22]=="3":
                            self.Bed22.setText("")
                            self.Bed22.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   
                   if(self.total_bed>22):
                        if self.status_arr[23]=="1":
                            self.Bed23.setText("")
                   if(self.total_bed>22):
                        if self.status_arr[23]=="2":
                            self.Bed23.setText("")
                            self.Bed23.setStyleSheet("color: Red; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   if(self.total_bed>22):
                        if self.status_arr[23]=="3":
                            self.Bed23.setText("")
                            self.Bed23.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   
                   if(self.total_bed>23):
                        if self.status_arr[24]=="1":
                            self.Bed24.setText("")
                   if(self.total_bed>23):
                        if self.status_arr[24]=="2":
                            self.Bed24.setText("")
                            self.Bed24.setStyleSheet("color: Red; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   if(self.total_bed>23):
                        if self.status_arr[24]=="3":
                            self.Bed24.setText("")
                            self.Bed24.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   
                   if(self.total_bed>24):
                        if self.status_arr[25]=="1":
                            self.Bed25.setText("")
                   if(self.total_bed>24):
                        if self.status_arr[25]=="2":
                            self.Bed25.setText("")
                            self.Bed25.setStyleSheet("color: Red; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   if(self.total_bed>24):
                        if self.status_arr[25]=="3":
                            self.Bed25.setText("")
                            self.Bed25.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   
                   if(self.total_bed>25):
                        if self.status_arr[26]=="1":
                            self.Bed26.setText("")
                   if(self.total_bed>25):
                        if self.status_arr[26]=="2":
                            self.Bed26.setText("")
                            self.Bed26.setStyleSheet("color: Red; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   if(self.total_bed>25):
                        if self.status_arr[26]=="3":
                            self.Bed26.setText("")
                            self.Bed26.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                            
                   if(self.total_bed>26):
                        if self.status_arr[27]=="1":
                            self.Bed27.setText("")
                   if(self.total_bed>26):
                        if self.status_arr[27]=="2":
                            self.Bed27.setText("")
                            self.Bed27.setStyleSheet("color: Red; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   if(self.total_bed>26):
                        if self.status_arr[27]=="3":
                            self.Bed27.setText("")
                            self.Bed27.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   
                   if(self.total_bed>27):
                        if self.status_arr[28]=="1":
                            self.Bed28.setText("")
                   if(self.total_bed>27):
                        if self.status_arr[28]=="2":
                            self.Bed28.setText("")
                            self.Bed28.setStyleSheet("color: Red; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   if(self.total_bed>27):
                        if self.status_arr[28]=="3":
                            self.Bed28.setText("")
                            self.Bed28.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   
                   if(self.total_bed>28):
                        if self.status_arr[29]=="1":
                            self.Bed29.setText("")
                   if(self.total_bed>28):
                        if self.status_arr[29]=="2":
                            self.Bed29.setText("")
                            self.Bed29.setStyleSheet("color: Red; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   if(self.total_bed>28):
                        if self.status_arr[29]=="3":
                            self.Bed29.setText("")
                            self.Bed29.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   
                   if(self.total_bed>29):
                        if self.status_arr[30]=="1":
                            self.Bed30.setText("")
                   if(self.total_bed>29):
                        if self.status_arr[30]=="2":
                            self.Bed30.setText("")
                            self.Bed30.setStyleSheet("color: Red; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   if(self.total_bed>29):
                        if self.status_arr[30]=="3":
                            self.Bed30.setText("")
                            self.Bed30.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   
                   if(self.total_bed>30):
                        if self.status_arr[31]=="1":
                            self.Bed31.setText("")
                   if(self.total_bed>30):
                        if self.status_arr[31]=="2":
                            self.Bed31.setText("")
                            self.Bed31.setStyleSheet("color: Red; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   if(self.total_bed>30):
                        if self.status_arr[31]=="3":
                            self.Bed31.setText("")
                            self.Bed31.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   
                   if(self.total_bed>31):
                        if self.status_arr[32]=="1":
                            self.Bed32.setText("")
                   if(self.total_bed>31):
                        if self.status_arr[32]=="2":
                            self.Bed32.setText("")
                            self.Bed32.setStyleSheet("color: Red; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   if(self.total_bed>31):
                        if self.status_arr[32]=="3":
                            self.Bed32.setText("")
                            self.Bed32.setStyleSheet("color: Blue; background-color: #B4D5D7; qproperty-alignment: AlignCenter;")
                   
                   

                   
                self.blink=0
                
        
        
        
        
                
                
            
    
if __name__ == '__main__':
    app = QApplication([])
    
    loop = QEventLoop()
    asyncio.set_event_loop(loop)
    

    
    app.setOrganizationName('Softech')
    app.setApplicationName('NTS-MDSOFT21 Ver1.2')
    mainWin = MainWindow()
    mainWin.show()
    
    #w = RemoteWidget()
   # w.show()
    #x=MainWindow()
   # x.update_label(time)
    with loop:
        loop.run_forever()      
        
