12
import unittest
import HTMLTestRunner
import time
from Test_Case.Unit_OnlineMedia import *
#from Test_Case.Unit_HudongRadio import *
import warnings

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    suite = unittest.TestSuite()
    warnings.filterwarnings('ignore')
    #tests = [HuDongRadio_Test("test_t1"),HuDongRadio_Test("test_t2"),HuDongRadio_Test("test_t3")]
    tests = [OnlineMedia_Test("test_t1"), OnlineMedia_Test("test_t2")]
    suite.addTests(tests)

    # runner = unittest.TextTestRunner(verbosity=2)

    # 1、获取当前时间，这样便于下面的使用。
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))

    # 2、html报告文件路径
    f = open("D:\\test.html", "wb")

    # 3、打开一个文件，将result写入此file中

    runner = HTMLTestRunner.HTMLTestRunner(stream=f,
                                           title=u'在线媒体自动化测试报告,测试结果如下：',
                                           description=u'用例执行情况：')
    runner.run(suite)
    f.close()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
