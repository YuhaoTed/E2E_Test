import unittest
import time
from playsound import playsound
from Fundament.Pic_Process import *
from Fundament.Snap_shot import *
from Fundament.P_can_test import *
import HTMLTestRunner
import shutil

class Test_Util():

    def __init__(self):
        self.Touch = None
        self.Pic = None
        self.Sc = None
    def Start(self):
        self.Touch = SerialThread()
        self.Pic = Pic_Pro()
        self.Sc = Snap_Shot()
        self.Touch.start()
        self.Sc.Connect()
        self.Sc.Get_png()
    def PrePare_img(self):
        self.Sc.Get_png()
        self.Pic.get_img()

    def Enter_app(self, App_name):
        # print("进入"+App_name)
        self.Sc.Get_png()
        self.Pic.get_img()
        flag = True
        cnt = 0
        coor = None
        while flag and cnt < 5:
            self.Touch.Touch_main()
            time.sleep(0.5)
            self.Sc.Get_png()
            self.Pic.get_img()
            tmp = self.Pic.Pic_OCR()
            for i in tmp:
                if App_name in i:
                    coor = i[0]
                    flag = False
                    break
            cnt += 1
        if coor == None:
            return False
        else:
            # print("kaishidianji app")
            self.Touch.Send_Touch_Command(coor[0][0], coor[0][1])
            time.sleep(1)
            return True

    def Find_Word(self, word,coor=None):
        tmp = self.Pic.Pic_OCR(coor=coor)
        x1 = 0
        y1 = 0
        if coor!=None:
            x1 = coor[0][0]
            y1 = coor[0][1]
        for i in tmp:
            for word1 in word:
                if word1 in i[1]:
                    i[0][0][0]+=x1
                    i[0][0][1]+=y1
                    return i[0]
        return False

    def Add_SC_Report(self, t1):
        # self.PrePare_img()
        shutil.copy('D:\software\pythonProject\SC\\1.PNG',
                    'D:\software\pythonProject\SAVE\\screenpicture' + t1 + '.PNG')
        print("开始截图：")
        print('D:\software\pythonProject\SAVE\\screenpicture' + t1 + '.PNG')

    def Find_Pop(self, Recongnize_Word, Action_word):
        self.PrePare_img()
        self.PrePare_img()
        if self.Pic.Find_Popup():
            if Recongnize_Word == None:
                tmp = self.Find_Word([Action_word])
                self.Touch.Send_Touch_Command(tmp[0].tmp[1])

    def Play_SDS(self,tar):
        playsound(tar)
#Test_Util_Basic = Test_Util()
global Test_Util1
Test_Util1 = Test_Util()
Test_Util1.Start()

