# conda create -n GrandPrix python=3.8
# conda activate GrandPrix 
# pip install opencv-python
# pip install pywin32
# pip install pynput
# pip install pyautogui
# conda install -c conda-forge scikit-image

import win32gui


def get_window_by_caption(caption):
    try:
        hwnd = win32gui.FindWindow(None, caption)
        return hwnd
    except Exception as ex:
        print('error calling win32gui.FindWindow ' + str(ex))
        return -1


# start
# =====

#nameWindows = "test.txt - Notepad"
nameWindows = 'Stella 6.5.2: "Grand Prix (1982) (Activision)"'


w = get_window_by_caption(nameWindows)
print (w)

if w > 0:
    win32gui.SetForegroundWindow( w )
else :
    print("Cannot find Atari window")
    
