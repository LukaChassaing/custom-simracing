import serial
from time import sleep
from directkeys import PressKey, ReleaseKey, DIK_F1, DIK_F2, DIK_F3, DIK_F4, DIK_F5, DIK_F6, DIK_F8, DIK_F10
import pyvjoy
import time
import re

print("pc2 profile\n")
s = serial.Serial('COM11')
j = pyvjoy.VJoyDevice(1)


while True:
    char = s.readline()
    # print(char)
    # print(char)
    if char == b'0\r\n':
        j.data.wAxisXRot = int(int(1023)*32.0303)
        j.update()
    else:
        j.data.wAxisXRot = 0
        j.update()
        if char == b'1\r\n':
            PressKey(DIK_F1)
            sleep(0.1)
            ReleaseKey(DIK_F1)
        if char == b'2\r\n':
            PressKey(DIK_F2)
            sleep(0.1)
            ReleaseKey(DIK_F2)
        if char == b'3\r\n':
            PressKey(DIK_F3)
            sleep(0.1)
            ReleaseKey(DIK_F3)
        if char == b'4\r\n':
            PressKey(DIK_F4)
            sleep(0.1)
            ReleaseKey(DIK_F4)
        if char == b'5\r\n':
            PressKey(DIK_F5)
            sleep(0.1)
            ReleaseKey(DIK_F5)
        if char == b'6\r\n':
            PressKey(DIK_F6)
            sleep(0.1)
            ReleaseKey(DIK_F6)
        if char == b'8\r\n':
            PressKey(DIK_F8)
            sleep(0.1)
            ReleaseKey(DIK_F8)
        if "e :" in str(char):
            #print("ici", char)
            nombres = re.findall(r'\b\d+\b', str(char))
            embrayage = nombres[0]
            embrayage =  1023 - int(embrayage)
            valeurFormatee = int(int(embrayage)*32.0303)
            print(valeurFormatee)
            j.data.wAxisXRot = valeurFormatee
            j.update()
        
    sleep(0.01)