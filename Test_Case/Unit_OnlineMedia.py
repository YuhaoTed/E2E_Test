import unittest
import time
from Fundament.Pic_Process import *
from Fundament.Snap_shot import *
from Fundament.P_can_test import *
import HTMLTestRunner
import shutil
class OnlineMedia_Test(unittest.TestCase):
    Touch = SerialThread()
    Pic = Pic_Pro()
    Sc = Snap_Shot()
    Touch.start()
    Sc.Connect()
    Sc.Get_png()
    def PrePare_img(self):
        self.Sc.Get_png()
        self.Pic.get_img()
    def Add_SC_Report(self,t1):
        #self.PrePare_img()
        shutil.copy('D:\software\pythonProject\SC\\1.PNG', 'D:\software\pythonProject\SAVE\\screenpicture'+t1+'.PNG')
        print("开始截图：")
        print('D:\software\pythonProject\SAVE\\screenpicture'+t1+'.PNG')
    def Enter_app(self,App_name):
        print("进入"+App_name)
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
            print("kaishidianji app")
            self.Touch.Send_Touch_Command(coor[0][0],coor[0][1])
            time.sleep(1)
            return True

    def Find_Word(self,word):
        tmp = self.Pic.Pic_OCR()
        for i in tmp:
            for word1 in word:
                if word1 in i[1]:
                    return True
        return False
    def test_t1(self):
        '''进入媒体 观察是否成功'''


        self.assertTrue(self.Enter_app("媒体"))
        self.PrePare_img()
        shutil.copy('D:\software\pythonProject\SC\\1.PNG','D:\software\pythonProject\SAVE\\screenpictureT1.PNG')
        print("D:\software\pythonProject\SAVE\\screenpictureT1.PNG")
    def test_t2(self):
        '''进入在线媒体'''
        '''判断是不是在在线媒体首页'''
        self.PrePare_img()
        tmp = self.Pic.Pic_Icon("D:\screenshots\\current.PNG")
        tmp = self.Pic.Pic_Icon("D:\screenshots\\kuwo.PNG")
        print(tmp)
        if tmp==None:
            time.sleep(1)
            self.Touch.Send_Touch_Command(61,145)
            time.sleep(1)
            self.Touch.Send_Touch_Command(306,482)
            time.sleep(5)
        else:
            time.sleep(5)
        self.Sc.Get_png()
        self.Pic.get_img()
        self.Add_SC_Report('t2')
        self.assertFalse(self.Find_Word(["失败","正在载入"]))

# if __name__ == 'Unit_OnlineMedia':
#     print(1)
#     suite = unittest.TestSuite()
#
#     tests = [OnlineMedia_Test("test_t1")]
#     suite.addTests(tests)
#
#     #runner = unittest.TextTestRunner(verbosity=2)
#
#     # 1、获取当前时间，这样便于下面的使用。
#     now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
#
#     # 2、html报告文件路径
#     f = open("D:\\test.html","wb")
#
#     # 3、打开一个文件，将result写入此file中
#
#     runner = HTMLTestRunner.HTMLTestRunner(stream=f,
#                                            title=u'在线媒体自动化测试报告,测试结果如下：',
#                                            description=u'用例执行情况：')
#     runner.run(suite)
#     f.close()

