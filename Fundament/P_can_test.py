# -*- coding: utf-8 -*-
import threading
import time
import serial
import binascii
#import serial.tools.list_ports
import datetime


class SerialThread:
    # 串口通讯默认参数
    usbSerial = serial.Serial()
    usbSerial.bytesize = serial.EIGHTBITS
    usbSerial.stopbits = serial.STOPBITS_ONE
    usbSerial.parity = serial.PARITY_NONE
    usbSerial.port = 'COM62'
    usbSerial.baudrate = 460800  # 460800
    #usbSerial.baudrate = 500000
    usbSerial.baudrate = 1500000  # 460800
    usbSerial.timeout = 1
    usbSerial.write_timeout = 1
    dataBuff = b''
    MaxDataLen = 32
    data = '66cc001130010217F8F17308'

    waitEnd = None
    alive = False
    thread_read = None

    def setSerialPort(self, Port):
        self.usbSerial.port = Port

    def setSerialPara(self, Port, Baudrate, Bytesize, Stopbits, Parity):
        self.usbSerial.bytesize = Bytesize
        self.usbSerial.stopbits = Stopbits
        self.usbSerial.parity = Parity
        self.usbSerial.port = Port
        self.usbSerial.baudrate = Baudrate

    def start(self):
        try:
            self.usbSerial.open()
        except Exception as se:
            print(str(se))
            return False
        if self.usbSerial.isOpen():
            self.waitEnd = threading.Event()
            self.alive = True
            #self.thread_read = None
            #self.thread_read = threading.Thread(target=self.Reader)
            #self.thread_read.setDaemon(1)
            #self.thread_read.start()
            #print(self.usbSerial.name + " start success!")
            return True
        else:
            print(self.usbSerial.name + " start fail!")
            return False

    def waiting(self):
        if not self.waitEnd is None:
            self.waitEnd.wait()

    def stop(self):
        self.alive = False
        if (self.thread_read != None):
            self.thread_read.join()
        if self.usbSerial.isOpen():
            self.usbSerial.close()
            return True

    # 获取串口名称列表, list[0] = 'ERROR'表示无法获得串口名
    def getComportList(self):
        nameList = ['ERROR']
        plist = list(serial.tools.list_ports.comports())

        if len(plist) <= 0:
            print("The Serial port can't find!")
            return nameList
        else:
            del nameList[0]
            for comports in plist:
                nameList.append(comports[0])
            return nameList

    # 发送数据
    def SendDate(self, msg):
        #         return True                 ######################
        # strData= str(binascii.b2a_hex(msg))
        ####        print("Send commandData:"+strData)
        #print(msg)
        isOK = False
        if (self.alive == True) and (self.usbSerial.writable()):
            lmsg = ''
            if isinstance(msg, str):
                #lmsg = msg.encode('gb18030')
                #lmsg = msg.encode('utf-8')
                lmsg=bytes.fromhex(msg)
                #print(lmsg)
            else:
                lmsg = msg
            try:
                # 发送数据到相应的处理组件
                # print(lmsg)
                self.usbSerial.write(lmsg)
                isOK = True
                #print("SerialThread sendData Success:"+(str)(datetime.datetime.now())[:-3])
            except Exception as ex:
                print("数据发送失败")
                pass
            return isOK
        else:
            print("数据发送失败，不可发送状态")
            return isOK

    # 将字节串转换为整数
    def bytesToInt(self, bytesData):
        size = len(bytesData)
        i = size
        result = 0
        while i > 0:
            result += (int)(bytesData[i - 1]) * 256 ** (size - i)
            i -= 1
        return result

    # 数据包校验
    def checkCommandData(self, data):
        checkDataSize = len(data) - 3  # 起始标志+包校验位 = 3
        sum = 0
        firstPos = 2

        while checkDataSize > 0:
            sum += (int)(data[firstPos])
            firstPos += 1
            checkDataSize -= 1
        sum = sum & 255  # 取与运算，只保留1Byte有效值
        if sum == data[len(data) - 1]:
            return True
        else:
            return False

    def dataPackageToQueue(self, data):
        self.dataBuff += data
        #         strData= str(binascii.b2a_hex(self.dataBuff))
        #print(self.dataBuff)
        firstPos = self.dataBuff.find(0x66)
        if (len(self.dataBuff) >= (firstPos + 6)):  # 数据长度足够最小指令长度， 起始标志+包长度+命令+校验 = 6
            while ((firstPos != -1) and (self.dataBuff[firstPos + 1] == 0xCC)):
                packageSize = self.bytesToInt(self.dataBuff[firstPos + 2:firstPos + 4])  # 起始标志 = 2，起始标志+包长度 = 4
                if (packageSize > self.MaxDataLen):  # 错误码导致帧长度过长，丢弃此帧数据
                    print('全部数据：' + str(binascii.b2a_hex(self.dataBuff)))
                    print('丢弃数据，帧长度过长：' + str(binascii.b2a_hex(self.dataBuff[0:firstPos + 1])))
                    self.dataBuff = self.dataBuff[firstPos + 1:]
                    break
                if (len(self.dataBuff) >= (firstPos + 4 + packageSize)):  # 数据已全部收全   起始标志+包长度 = 4
                    commandData = self.dataBuff[firstPos:firstPos + 4 + packageSize]  # 起始标志+包长度 = 4
                    self.dataBuff = self.dataBuff[firstPos + 4 + packageSize:]  # 截取字符串
                    if self.checkCommandData(commandData) == True:
                        #                         print('CommandData check OK:'+str(binascii.b2a_hex(commandData)))   #################
                        #                         self.readBuffQueue.put(commandData)                                                        #暂不放入Buffer
                        self.cDInstance.__getattribute__(self.cDFunctionName)(commandData)
                        # self.cDInstance.__getattribute__(self.cDFunctionName)(params)
                    else:
                        print("Error:Get Data but checkSum is wrong." + str(binascii.b2a_hex(commandData)))
                        print('丢弃数据，校验位错误：' + str(binascii.b2a_hex(commandData)))
                else:
                    break

                # 继续查询新的指令
                firstPos = self.dataBuff.find(0x66)
                if (len(self.dataBuff) < (firstPos + 5)):
                    break
            #             strData= str(binascii.b2a_hex(self.dataBuff))
            firstPos = self.dataBuff.find(0x66)
            #             print("strData ="+strData+" , firstPos ="+(str)(firstPos))
            if (len(self.dataBuff) >= (firstPos + 6)):
                if ((firstPos != -1) and (self.dataBuff[firstPos + 1] != 0xCC)):
                    print('全部数据：' + str(binascii.b2a_hex(self.dataBuff)))
                    print('丢弃数据，XXXXX：' + str(binascii.b2a_hex(self.dataBuff[0:firstPos + 1])))
                    self.dataBuff = self.dataBuff[firstPos + 1:]  # 截取0x66（包含）之前无效字符

    def Reader(self):
        while self.alive:
            time.sleep(0.001)
            data = ''
            #data = data.encode('utf-8')

            try:
                n = self.usbSerial.inWaiting()
                if n:
                    data = self.usbSerial.read(n)
                    print(data)
            except:
                self.alive = False
                print("Oops!  串口读取错误。")
                self.usbSerial.close()
                break

            if (len(data) > 0):
                print()
                #print(strData)        #print("Serial Get commandData  = " +strData)
                #self.dataPackageToQueue(data)

        self.waitEnd.set()
        self.alive = False

    def Cal_Xy2Signal(self,x, y):
        Signal_value = 59911  # EA07
        if x > 639:
            x = 639
        if y > 319:
            y = 319
        # y+=48
        # 计算x的数值
        tmp_x = x % 4
        Signal_value += tmp_x * 2 ** 30
        x -= tmp_x
        tmp_x_1 = int(x / 4)
        Signal_value += tmp_x_1 * 2 ** 16
        if y > 255:
            y -= 256
            Signal_value += 2 ** 28
            tmp_y = y % 16
            Signal_value += tmp_y * 2 ** 36
            tmp_y_1 = int(y / 16)
            Signal_value += tmp_y_1 * 2 ** 24
            return Signal_value
        else:
            tmp_y = y % 16
            Signal_value += tmp_y * 2 ** 36
            tmp_y_1 = int(y / 16)
            Signal_value += tmp_y_1 * 2 ** 24
            return Signal_value
    def Cal_str(self,x,y,flag,x_dir=0,y_dir=0):
        x = int(x / 1280 * 639)
        y = int(y / 631 * 319)
        if flag==0:
            #1：按下
            tmp = str(hex(self.Cal_Xy2Signal(x, y)+2*2**32))[2:].upper()
        elif flag==1:
            #0:抬起
            tmp = str(hex(self.Cal_Xy2Signal(x, y)))[2:].upper()
        elif flag ==2:
            tmp = str(hex(self.Cal_Xy2Signal(x, y) + 4 * 2 ** 32))[2:].upper()

        if len(tmp)==9:
            tmp = "0"+tmp
        tmp1 = ""
        k = len(tmp) - 1
        while k > 0:
            tmp1 += tmp[k - 1:k + 1]
            k -= 2
        for i in range(0, (16 - len(tmp))):
            tmp1 += "0"
        if flag==2:
            tmp1 = tmp1[:-1]
            tmp1 = tmp1+"2"
            if x_dir>0:
                tmp1 = tmp1[0:11]+'2'+tmp1[12:]
            if x_dir<0:
                tmp1 = tmp1[0:10]+'DF'+tmp1[12:]
            if y_dir>0:
                tmp1 = tmp1[0:13]+'2'+tmp1[14:]
            if y_dir<0:
                tmp1 = tmp1[0:12]+'DF'+tmp1[14:]
        self.data += tmp1
        #print("计算值x"+"..."+str(x)+"计算值y..."+str(y)+"..."+tmp1+"...x_dir"+str(x_dir)+"...y_dir"+str(y_dir))
    def Cal_crc(self):
        start_byte = 4
        sum = 0
        #print(self.data)
        while start_byte < len(self.data):
            if ord(self.data[start_byte]) < 58:
                sum += int(self.data[start_byte]) * 16
            else:
                sum += ((ord(self.data[start_byte]) - ord('A')) + 10) * 16
            if ord(self.data[start_byte + 1]) < 58:
                sum += int(self.data[start_byte + 1])
            else:
                sum += ((ord(self.data[start_byte + 1]) - ord('A')) + 10)
            start_byte += 2
        sum %= 256
        if len(str(hex(sum)))==3:
            self.data += '0'
            self.data += str(hex(sum))[2:].upper()
        else:
            self.data += str(hex(sum))[2:].upper()

    def Send_Touch_Command(self,x,y):
        #self.data+=str(hex(self.Cal_Xy2Signal(x,y)))[2:].upper()
        self.Cal_str(x,y,0)
        self.Cal_crc()
        #print("开始按下"+self.data)
        self.SendDate(self.data)
        self.data = "66cc001130010217F8F17308"
        time.sleep(0.5)
        self.Cal_str(x, y,1)
        self.Cal_crc()
        #print("开始抬起" + self.data)
        self.SendDate(self.data)
        self.data = "66cc001130010217F8F17308"
        return True
    def Touch_main(self):

        self.data += "04301A0100AAAAAA"
        self.Cal_crc()
        self.SendDate(self.data)
        time.sleep(1)
        self.data = "66cc001130010217F8F17308"
        self.data += "04301A000BAAAAAA"
        self.Cal_crc()
        print('开始点击Main')
        self.SendDate(self.data)
        self.data = "66cc001130010217F8F17308"
        return True
    def Send_Slide_Command(self,x,y,xdir,ydir):

        self.Cal_str(x, y, 2,xdir,ydir)
        self.Cal_crc()
        #print("开始按下" + self.data)
        self.SendDate(self.data)
        self.data = "66cc001130010217F8F17308"
    def Slide(self,Start_x,Start_y,End_x,End_y):
        # Start_x = int(Start_x / 1280 * 639)
        # Start_y = int(Start_y / 631 * 319)
        # End_x = int(End_x / 1280 * 639)
        # End_y = int(End_y / 631 * 319)
        step_x = int((End_x-Start_x)/3)
        x_dir = 0
        y_dir = 0
        if step_x>0:
            x_dir = 2
        elif step_x<0:
            x_dir = -2

        step_y = int((End_y-Start_y)/3)
        if step_y>0:
            y_dir = 2
        elif step_y>0:
            y_dir = -2
        step = max(abs(step_x),abs(step_y))
        step_len_x = int((End_x-Start_x)/step)
        step_len_y = int((End_y-Start_y)/step)
        #print(step_x,step_len_x,Start_x,End_x)
        #点击
        self.Cal_str(Start_x, Start_y, 0)
        self.Cal_crc()
        # print("开始按下"+self.data)
        self.SendDate(self.data)
        self.data = "66cc001130010217F8F17308"
        time.sleep(0.01)
        ###
        for i in range(0,step):
            self.Send_Slide_Command(Start_x,Start_y,x_dir,y_dir)
            time.sleep(0.005)
            Start_x+=step_len_x
            Start_y+=step_len_y
        #print(Start_x)
        # 点击
        self.Cal_str(Start_x, Start_y, 1)
        self.Cal_crc()
        # print("开始按下"+self.data)
        self.SendDate(self.data)
        self.data = "66cc001130010217F8F17308"
        time.sleep(0.01)
        return True
        ###

# ##17F8F173x Id


