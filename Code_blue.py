import os 
import sys
import os.path
import csv
import time
from os import path
from csv import writer
from PyQt5 import QtCore



try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0

flag1=0
flag2=0
flag3=0



def timerEvent():
    global time
    global flag1
    global flag2
    global flag3
    
    
    time = time.addSecs(1)
    
    
            

    
    config = ConfigParser()
    config.read("/home/pi/Share_Folder/my.ini")
    
    Code_room1=config['Code_Blue'].get('Room_no_1')
    Code_room2=config['Code_Blue'].get('Room_no_2')
    Code_room3=config['Code_Blue'].get('Room_no_3')
    Code_room4=config['Code_Blue'].get('Room_no_4')
    Code_room5=config['Code_Blue'].get('Room_no_5')
    
    Code_room6=config['Code_Emergency'].get('Room_no_1')
    Code_room7=config['Code_Emergency'].get('Room_no_2')
    Code_room8=config['Code_Emergency'].get('Room_no_3')
    Code_room9=config['Code_Emergency'].get('Room_no_4')
    Code_room10=config['Code_Emergency'].get('Room_no_5')
    
    Code_room11=config['Code_Normal'].get('Room_no_1')
    Code_room12=config['Code_Normal'].get('Room_no_2')
    Code_room13=config['Code_Normal'].get('Room_no_3')
    Code_room14=config['Code_Normal'].get('Room_no_4')
    Code_room15=config['Code_Normal'].get('Room_no_5')
    
    
    list = []
    list = [Code_room1, Code_room2, Code_room3, Code_room4, Code_room5, Code_room6, Code_room7, Code_room8, Code_room9, Code_room10, Code_room11, Code_room12, Code_room13, Code_room14, Code_room15]
    
    
    
    
    for j in range(len(list)):
        #print(" value  : "+str(list[j]))
        for j in range(0,5):
            if list[j]!='':
                flag1=1
                       
        for j in range(5,10):#len(list)):
            if list[j]!='':
                flag2=1
                
        for j in range(10,15):#len(list)):
            if list[j]!='':
                flag3=1
                
    
    
        
        
            
    print("flag 1 : " +str(flag1))
    print("flag 2 : " +str(flag2))
    print("flag 3 : " +str(flag3))
    
                
    if flag1==1:
        flag2=0
        flag3=0
        for j in range(0,5):
            print(list[j])
            if list[j]!='':
                Bedno = "/home/pi/NewFolder/testing/mp3files/CODE_BLUE.mp3"
                os.system("mpg321 "+Bedno)
                Bedno2 = "/home/pi/NewFolder/testing/mp3files/BEDNO.mp3"
                os.system("mpg321 "+Bedno2)
                for i in list[j]:
                    if i !=0:
                        for value in i:
                            audio_string= "/home/pi/NewFolder/testing/mp3files/"+value+".mp3"
                            os.system("mpg321 "+audio_string)
        
    
    
    
    
    if flag2==1:
        flag3=0
        for j in range(5,10):
            if list[j]!='':
                Bedno = "/home/pi/NewFolder/testing/mp3files/EMERGENCYCALL.mp3"
                os.system("mpg321 "+Bedno)
                
                for i in list[j]:
                    if i !=0:
                        for value in i:
                            audio_string= "/home/pi/NewFolder/testing/mp3files/"+value+".mp3"
                            os.system("mpg321 "+audio_string)
        os.system("mpg321 "+"/home/pi/NewFolder/testing/mp3files/washroom.mp3")
    
    if flag3==1:
        for j in range(10,15):
            if list[j]!='':
                Bedno = "/home/pi/NewFolder/testing/mp3files/call.mp3"
                os.system("mpg321 "+Bedno)
                for i in list[j]:
                    if i !=0:
                        for value in i:
                            audio_string= "/home/pi/NewFolder/testing/mp3files/"+value+".mp3"
                            os.system("mpg321 "+audio_string)
                            
                            
            
    flag1=0
    flag2=0
    flag3=0 
        
        
        
        
app = QtCore.QCoreApplication(sys.argv)

timer = QtCore.QTimer()
time = QtCore.QTime(0, 0, 0)

timer.timeout.connect(timerEvent)
timer.start(1000)



sys.exit(app.exec_())