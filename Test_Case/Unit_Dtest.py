import unittest
import time
#from Fundament.Pic_Process import *
#from Fundament.Snap_shot import *
#from Fundament.P_can_test import *
#from Test_Case.Test_Util import *
import HTMLTestRunner
import shutil
#global Test_Util
from main import *
global Test_Util1
class HuSDS_Test(unittest.TestCase):

    #TU = Test_Util()

    #TU = Test_Util1
    #TU.Touch.Touch_main()
    #Test_Util1.Touch.Touch_main()
    def test_t1(self):
        '''进入互动电台 观察是否存在异常'''
        print('touch1')
        Test_Util1.Touch.Touch_main()
        print('touch2')
        Test_Util1.Touch.Send_Touch_Command(641, 47)
        self.assertTrue(Test_Util1.Enter_app("互动电台"))
        time.sleep(2)
        print("1.进入互动电台")
        self.Add_SC_Report("t1")
        self.assertFalse(self.TU.Find_Word(["失败", "正在载入"]))
        print("2.检查是否存在失败等异常")





