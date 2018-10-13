import cv2
import numpy as nu
from pynput.mouse import Button, Controller
import wx
import time


oldtime = time.time()
window = wx.App(False)

(screenX, screenY) = wx.GetDisplaySize()

(camX, camY) = (340, 280)

L_range = nu.array([33, 80, 40])
U_range = nu.array([102, 255, 255])

camera = cv2.VideoCapture(0)
camera.set(3, camX)
camera.set(4, camY)

Open = nu.ones((5, 5))
Close = nu.ones((20, 20))

click_Flag = 0
openX, openY, openW, openH = (0, 0, 0, 0)

mouse = Controller()

old_mouse_Cord = nu.array([0, 0])
mouse_location = nu.array([0, 0])
mouse_speed_facotr = 2

while True:
    ret, img = camera.read()

    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(imgHSV, L_range, U_range)

    maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, Open)
    maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, Close)

    maskFinal = maskClose
    _, conts, h = cv2.findContours(maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)



    if len(conts) == 2:




        if click_Flag == 1:
            click_Flag = 0
            mouse.release(Button.left)

        x1, y1, w1, h1 = cv2.boundingRect(conts[0])
        x2, y2, w2, h2 = cv2.boundingRect(conts[1])
        cv2.rectangle(img, (x1, y1), (x1 + w1, y1 + h1), (255, 0, 0), 2)
        cv2.rectangle(img, (x2, y2), (x2 + w2, y2 + h2), (255, 0, 0), 2)

        cx1 = (x1 + w1 // 2)
        cy1 = (y1 + h1 // 2)
        cx2 = (x2 + w2 // 2)
        cy2 = (y2 + h2 // 2)
        cx = ((cx1 + cx2) // 2)
        cy = ((cy1 + cy2) // 2)

        cv2.line(img, (cx1, cy1), (cx2, cy2), (255, 0, 0), 2)
        cv2.circle(img, (cx, cy), 2, (0, 0, 255), 2)

        mouse_location = old_mouse_Cord + ((cx, cy) - old_mouse_Cord) // mouse_speed_facotr

        mouse.position = (screenX - (mouse_location[0] * screenX // camX), mouse_location[1] * screenY // camY)

        while mouse.position != (screenX - (mouse_location[0] * screenX // camX), mouse_location[1] * screenY // camY):
            pass

        old_mouse_Cord = mouse_location
        openX, openY, openW, openH = cv2.boundingRect(nu.array([[[x1, y1], [x1 + w1, y1 + h1], [x2, y2], [x2 + w2, y2 + h2]]]))




    elif len(conts) == 1:
        x, y, w, h = cv2.boundingRect(conts[0])
        if click_Flag == 0:
            if abs((w * h - openW * openH) * 100 // (w * h)) < 50:
                click_Flag = 1
                mouse.press(Button.left)


                openX, openY, openW, openH = (0, 0, 0, 0)

        else:

            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cx = int(x + w / 2)
            cy = int(y + h / 2)
            cv2.circle(img, (cx, cy), (w + h) // 4, (0, 0, 255), 2)

            mouse_location = old_mouse_Cord + ((cx, cy) - old_mouse_Cord) // mouse_speed_facotr

            mouse.position = (screenX - (mouse_location[0] * screenX // camX), mouse_location[1] * screenY // camY)

            while mouse.position != (screenX - (mouse_location[0] * screenX // camX), mouse_location[1] * screenY // camY):
                pass

            old_mouse_Cord = mouse_location


    cv2.imshow("camera", img)
    cv2.waitKey(5)
