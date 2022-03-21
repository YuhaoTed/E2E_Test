from Test_Case.Testcase_Para import *
from Test_Case.Test_Util import *
import sys

sys.path.append("path")
import unittest
import time
from Fundament.Pic_Process import *
from Fundament.Snap_shot import *
from Fundament.P_can_test import *
import HTMLTestRunner
import shutil


class Unit_Btest(ParametrizedTestCase):
    Test_Util1 = Test_Util()

    def test_B1(self):
        ''' 测试一下参数化'''
        Test_Util1 = self.param
        Test_Util1.Touch.Send_Touch_Command(100, 200)
        self.assertTrue(Test_Util1.Enter_app('收音机'))
        shutil.copy('D:\software\pythonProject\SC\\1.PNG', 'D:\software\pythonProject\SAVE\\screenpictureT1.PNG')
        print("D:\software\pythonProject\SAVE\\screenpictureT1.PNG")
