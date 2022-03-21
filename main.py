
import unittest

import time
#from Test_Case.Unit_OnlineMedia import *
#from Test_Case.Unit_HudongRadio import *
import warnings
import HTMLTestRunner
#from Test_Case.Unit_Atest import *
#from Test_Case.Unit_Btest import *
#from Test_Case.Testcase_Para import *
from Test_Case.Test_Util import *
#from Fundament.Test_Case_Parse import *
from Test_Case.Unit_Ctest import *
from Test_Case.Unit_Dtest import *
# Press the green button in the gutter to run the script.

if __name__ == '__main__':


    # Test_Util1 = Test_Util()
    # Test_Util1.Start()
    # Test_Util1.Touch.Touch_main()
    #正常的suite
    
    suite = unittest.TestSuite()
    #warnings.filterwarnings('ignore')
    #tests = [HuDongRadio_Test("test_t1"),HuDongRadio_Test("test_t2"),HuDongRadio_Test("test_t3")]
    #tests = [OnlineMedia_Test("test_t3"), OnlineMedia_Test("test_t4"),OnlineMedia_Test("test_t5"),OnlineMedia_Test("test_t6")]
    tests = [HuNavi_Test("test_t1"),HuSDS_Test("test_t1")]
    suite.addTests(tests)


    '''测试suite'''
    # suite1 = unittest.TestSuite
    # Test_Util_Common  = Test_Util()
    # suite1.addTest(ParametrizedTestCase.parametrize(Unit_Atest('test_A1')))
    # suite1.addTest(ParametrizedTestCase.parametrize(Unit_Btest('test_B1')))
    # runner = unittest.TextTestRunner(verbosity=2)
    # res = []
    # TestCaseParse("Test_Config.xml",res)
    #func = globals().get(func_name)
    # 1、获取当前时间，这样便于下面的使用。
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))

    # 2、html报告文件路径
    f = open("D:\\test.html", "wb")

    # 3、打开一个文件，将result写入此file中

    runner = HTMLTestRunner.HTMLTestRunner(stream=f,
                                           title=u'Smoke Test 自动化测试报告,测试结果如下：',
                                           description=u'用例执行情况：')
    runner.run(suite)
    f.close()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
