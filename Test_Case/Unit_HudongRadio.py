import unittest
import time
from Fundament.Pic_Process import *
from Fundament.Snap_shot import *
from Fundament.P_can_test import *
import HTMLTestRunner
import shutil
class HuDongRadio_Test(unittest.TestCase):
    Touch = SerialThread()
    Pic = Pic_Pro()
    Sc = Snap_Shot()
    Touch.start()
    Sc.Connect()
    Sc.Get_png()
    def PrePare_img(self):
        self.Sc.Get_png()
        self.Pic.get_img()

    def Enter_app(self,App_name):
        #print("进入"+App_name)
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
            cnt+=1
        if coor == None:
            return False
        else:
            #print("kaishidianji app")
            self.Touch.Send_Touch_Command(coor[0][0],coor[0][1])
            time.sleep(1)
            return True

    def Find_Word(self,word):
        tmp = self.Pic.Pic_OCR()
        for i in tmp:
            for word1 in word:
                if word1 in i[1]:
                    return i[0]
        return False

    def Add_SC_Report(self,t1):
        #self.PrePare_img()
        shutil.copy('D:\software\pythonProject\SC\\1.PNG', 'D:\software\pythonProject\SAVE\\screenpicture'+t1+'.PNG')
        print("开始截图：")
        print('D:\software\pythonProject\SAVE\\screenpicture'+t1+'.PNG')
    def Find_Pop(self,Recongnize_Word,Action_word):
        self.PrePare_img()
        self.PrePare_img()
        if self.Pic.Find_Popup():
            if Recongnize_Word==None:
                tmp = self.Find_Word([Action_word])
                self.Touch.Send_Touch_Command(tmp[0].tmp[1])

    def test_t1(self):
        '''进入互动电台 观察是否存在异常'''


        self.assertTrue(self.Enter_app("互动电台"))
        time.sleep(2)
        print("1.进入互动电台")
        self.Add_SC_Report("t1")
        self.assertFalse(self.Find_Word(["失败", "正在载入"]))
        print("2.检查是否存在失败等异常")
    def test_t2(self):
        '''点击发现，观察是否存在异常'''
        self.Touch.Send_Touch_Command(68,118)
        time.sleep(0.5)
        self.PrePare_img()
        self.assertFalse(self.Find_Word(["失败", "正在载入"]))
        print("1. 点击发现，观察是否存在异常")
        self.Add_SC_Report('t2')
    def test_t3(self):
        '''点击推荐，左右滑动观察有无异常'''
        self.Find_Pop(None,"取消")
        '''点击发现'''
        self.Touch.Send_Touch_Command(68, 118)
        time.sleep(0.5)
        self.PrePare_img()
        self.assertFalse(self.Find_Word(["失败", "正在载入"]))
        print("1. 点击发现，观察是否存在异常")
        self.Add_SC_Report('t3')
        '''点击推荐'''
        self.Touch.Send_Touch_Command(240, 134)
        time.sleep(0.5)
        self.PrePare_img()
        self.assertFalse(self.Find_Word(["失败", "正在载入","异常"]))
        print("2. 点击推荐，观察是否存在异常")
        self.Add_SC_Report('t4')
        '''向左划动'''
        while self.Find_Word(["更多"])==False:
            self.Find_Pop(None, "取消")
            #左划
            self.Touch.Slide(1215,345,194,345)
            time.sleep(1)
            self.PrePare_img()
            self.assertFalse(self.Find_Word(["失败", "正在载入", "异常"]))
            print("3. 左右滑动，观察是否存在异常")
            self.Add_SC_Report('t5')





