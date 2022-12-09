#conda create -n pianoTilesGame python=3.7
#conda activate pianoTilesGame

#####pip install pywin32
#####conda install pywin32
#pip install keyboard
#pip install pyautogui
#pip install opencv-python
#pip install mouse

from pyautogui import *
import pyautogui
import time
import keyboard
import random
import mouse
import beepy

#import win32con
#import win32api


# check what is the color under the mouse pointer
#pyautogui.displayMousePosition()

# my game position

Xpos1 = 1424
Xpos2 = 1622
Xpos3 = 1820
Xpos4 = 2034



Y = 800

def mouseClick(x, y):
    mouse.move("1424","800")
    mouse.click(button='left')
    
    # win32api.setCursorPos((x,y))
    # win32api.SetCursorPos
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    # time.sleep(0.01)
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    

while keyboard.is_pressed('q') ==False :
    #print(pyautogui.pixel(Xpos1,Y))
    if pyautogui.pixel(Xpos1,Y) == (0,0,0): # check if the pixel in the 1 position is black
        beepy.beep(sound="ping")
        mouseClick(Xpos1,Y)
    
    if pyautogui.pixel(Xpos2,Y) == (0,0,0): # check if the pixel in the 1 position is black
        print('Black2')
        mouseClick(Xpos2,Y)
    
    if pyautogui.pixel(Xpos3,Y) == (0,0,0): # check if the pixel in the 1 position is black
        print('Black3')
        mouseClick(Xpos3,Y)
    
    if pyautogui.pixel(Xpos4,Y) == (0,0,0): # check if the pixel in the 1 position is black
        print('Black4')
        mouseClick(Xpos4,Y)



