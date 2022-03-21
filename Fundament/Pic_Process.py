import cv2
import numpy as np
import easyocr
import time
import pyzbar.pyzbar as pyzbar

class Pic_Pro:

    img = cv2.imread('D:\\software\\pythonProject\\SC\\1.PNG')
    Icon_img = None
    reader = easyocr.Reader(['ch_sim', 'en'])

    def get_img(self):
        self.img = cv2.imread('D:\\software\\pythonProject\\SC\\1.PNG')
        #"D:\screenshots\\avartar.PNG"
        #self.img = cv2.imread("D:\screenshots\\T9.PNG")
    def Pic_OCR(self,coor=None):
        #coor[[x1,y1],[x2,y2]] 1：左上角 2：右下角
        #return self.reader.readtext(self.img[0:375, 240:480])
        #self.img = cv2.imread('D:\\1.PNG')
        if coor!=None:
            return self.reader.readtext(self.img[coor[0][0]:coor[1][0],coor[0][1]:coor[1][1]])
        else:
            return self.reader.readtext(self.img)
    def Pic_Icon(self,icon):
        # 读取目标图片
        #print(1)
        #self.img = cv2.imread('D:\\1.PNG')
        # 读取模板图片
        min_val_tmp = 2
        min_loc_tmp = None
        for i in icon:
            self.Icon_img = cv2.imread(icon)
            result = cv2.matchTemplate(self.img, self.Icon_img, cv2.TM_SQDIFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            #print(min_val)
            if min_val<min_val_tmp:
                min_val_tmp = min_val
                min_loc_tmp = min_loc
        print(min_val)
        if min_val<0.1:
            return min_loc
        else:
            return None
    def Find_Popup(self):
        self.get_img()
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([110, 30, 40])
        upper_blue = np.array([120, 40, 50])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        res = cv2.bitwise_and(self.img, self.img, mask=mask)
        frame_cvt = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(frame_cvt, 13, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours( frame_cvt,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )
        print(contours)
        print(len(contours))
        l_wid = 0
        l_height = 0
        for i in contours:
            if len(i)>3:
                t_wid = i[2][0][0]-i[0][0][0]
                t_height = i[2][0][1]-i[0][0][1]
            else:
                continue
            if  l_wid==0:
                l_wid = t_wid
                l_height = t_height
            elif t_wid>=l_wid and t_height>=l_height:
                l_wid = t_wid
                l_height = t_height
        print(l_wid,l_height)
        if l_wid>900 and l_height>200:
            print("有POP  UP")
            return True
        else:
            print("无POP UP")
            return False
    def Find_QR(self):
        test = pyzbar.decode(self.img)
        if test==None:
            print("无二维码")
            return False
        else:
            print("有二维码")
            return True
    def Find_Cursor(self,Scope,Orientation,Section):
        X_Min = Scope[0]
        X_Max = Scope[1]
        Y_Min = Scope[2]
        Y_Max = Scope[3]
        Img_Tmp = self.img[Y_Min:Y_Max,X_Min:X_Max]
        hsv = cv2.cvtColor(Img_Tmp, cv2.COLOR_BGR2HSV)
        # define range of blue color in HSV
        lower_blue = np.array([1, 50, 30])
        upper_blue = np.array([225, 225, 225])
        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(Img_Tmp, Img_Tmp, mask=mask)
        frame_cvt = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(frame_cvt, 100, 255, cv2.THRESH_BINARY)
        # frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # ret, thresh = cv.threshold(frame, 13, 255, cv.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(frame_cvt, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        Left_x = 10000
        Left_y = 10000
        Top_x = 0
        Top_y = 0
        for Contour in contours:
            for Point in Contour:
                if Point[0][0]<Left_x:
                    Left_x = Point[0][0]
                    Left_y = Point[0][1]
                if Point[0][1]>Top_y:
                    Top_x = Point[0][0]
                    Top_y = Point[0][1]
        if Orientation==1:
            #横向
            Section_Width = int(X_Max-X_Min)/Section
            return int(Left_x/Section_Width)+1
        if Orientation==2:
            #纵向
            Section_Height = int(Y_Max-Y_Min)/Section
            return int(Top_y/Section_Height)+1
        return False
                