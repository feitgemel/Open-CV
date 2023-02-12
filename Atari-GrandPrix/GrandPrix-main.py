
# conda create -n GrandPrix python=3.8
# pip install opencv-python
# pip install pywin32
# pip install pynput
# pip install pyautogui
# conda install -c conda-forge scikit-image


import cv2
import numpy as np
import win32gui 
import win32con
import time
import pyautogui

nameWindows = 'Stella 6.5.2: "Grand Prix (1982) (Activision)"'
from pynput.keyboard import Key, Controller
keyboard = Controller()  

def get_window_by_caption(caption):
    try:
        hwnd = win32gui.FindWindow(None, caption)
        return hwnd
    except Exception as ex:
        print('error calling win32gui.FindWindow ' + str(ex))
        return -1

AtariWindowsHandle = get_window_by_caption(nameWindows)
if AtariWindowsHandle > 0:
    # SetWindowPos(hWnd, InsertAfter, X, Y, new width, new height, Flags)
    print(AtariWindowsHandle)
    win32gui.SetWindowPos(AtariWindowsHandle,win32con.HWND_TOPMOST,100,100,200,200,0)
    win32gui.SetForegroundWindow( AtariWindowsHandle )
    
else :
    print("Error capture windows")


def takeScreenshot(xScr , ySrc , wSrc , hSrc ):
    
    #print(xScr , ySrc , wSrc , hSrc)
    im = pyautogui.screenshot(region=(xScr,ySrc, wSrc, hSrc))
    
    # convert to numpy image
    CapImage = np.array(im)
    CapImageCV2 = cv2.cvtColor(CapImage, cv2.COLOR_RGB2BGR)

    return CapImageCV2



#Checking two images for shape similarity with OpenCV
from skimage.metrics import structural_similarity

def checkImagesSimilarity(savedCar , image2):

    savedCar_gray = cv2.cvtColor(savedCar, cv2.COLOR_BGR2GRAY)
    second_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    
    # Compute SSIM between two images
    score, diff = structural_similarity(savedCar_gray, second_gray, full=True)
    

  
    return score


def checkIsTheCarRedColor(img):

    lower_red = np.array([0, 0, 128], dtype = "uint8") 
    upper_red= np.array([40, 40, 220], dtype = "uint8")

    mask = cv2.inRange(img, lower_red, upper_red)
    detected_output = cv2.bitwise_and(img, img, mask =  mask) 


    blueChannel =detected_output[:,:,0]
    greenChannel =detected_output[:,:,1]
    redhannel =detected_output[:,:,2]  

    # check if red 
    if np.max(redhannel ) <=220 and np.max(greenChannel) <= 40 and np.max(blueChannel) <= 40  :
        return True
    else :
        return False

#####################################################
# start 

# Get windows dimenations 
x , y , w , h   = win32gui.GetWindowRect(AtariWindowsHandle)
#print (x , y , w , h )
MyCarArea_Adujst_Height = 120
MyCarArea_Adujst_Width = 50


# Grab my car (Need for compare to other cars during detection)
mySavedCarImage = cv2.imread("Open-CV/Atari-GrandPrix/MyCar.jpg")

    
while True :

    OriginalImage = takeScreenshot(x + 40, y + 30 , w - 130, h - 180 )
    #OriginalImage = takeScreenshot(x , y  , w , h  )
    win32gui.SetForegroundWindow( AtariWindowsHandle )

    OriginalImageHeight = OriginalImage.shape[0]
    OriginalImageWidth = OriginalImage.shape[1]


    roi = OriginalImage.copy()[MyCarArea_Adujst_Height:OriginalImageHeight-MyCarArea_Adujst_Height,
                                 MyCarArea_Adujst_Width:300]

    gray = cv2.cvtColor(roi,cv2.COLOR_RGB2GRAY)
    _,thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
    MyCarBlurred = cv2.GaussianBlur(thresh.copy(),(9,9),0)
    #canny = cv2.Canny(blurred_image,200,255)

    contours, hierachy = cv2.findContours(MyCarBlurred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # my car
    #------- 
    myxCarPox=0
    myyCarPox=0
    mywidthCntl=0
    myheightCnt=0

    # loop over each contour to find my car.
    for objectNumerator , cnt in enumerate(contours):

        #print(cv2.contourArea(cnt))
        

        # Make sure the contour area is somewhat higher than some threshold to make sure its a car and not some noise.
        if cv2.contourArea(cnt) > 5000 :
            #print(cv2.contourArea(cnt))
            # Retrieve the bounding box coordinates from the contour.
            xCarPox, yCarPox, widthCntl, heightCnt = cv2.boundingRect(cnt)
            yCntl = yCarPox + MyCarArea_Adujst_Height
            xCnt = xCarPox + MyCarArea_Adujst_Width
            
            
            # lest grab the car and calcultae our avarage color values
            roiCar = OriginalImage.copy()[yCntl:yCntl + heightCnt, xCnt:xCnt + widthCntl]

            # check if the object is myCar - 3 checks
            # image dimations 
            sameImageShape=False
            if mySavedCarImage.shape == roiCar.shape :
                sameImageShape = True
            
            #  car shape 
            sameCarShape=False
            if sameImageShape: # if the images are the same shape , and check the cars shape
                carScore = checkImagesSimilarity(mySavedCarImage,roiCar)
                if carScore >= 0.90 :
                    sameCarShape=True

            # red color
            SameColor = checkIsTheCarRedColor(roiCar)

            # print all three tests
            #print (sameImageShape, sameCarShape , SameColor) 

            # if all True than draw rectangle
            if sameImageShape and sameCarShape and SameColor :
                cv2.rectangle(OriginalImage, (xCnt , yCntl), (xCnt + widthCntl, yCntl + heightCnt),(0, 0, 255), 2)
                myxCarPox=xCarPox
                myyCarPox=yCarPox
                mywidthCntl=widthCntl
                myheightCnt=heightCnt
                #print(myxCarPox,myyCarPox,mywidthCntl,myheightCnt)

            
    # the rest of the area
    # =====================
    roiRest = OriginalImage.copy()[MyCarArea_Adujst_Height:OriginalImageHeight-MyCarArea_Adujst_Height,
                                 301:OriginalImageWidth-50]
    
    roiRest_width = roiRest.shape[1]
    roiRest_height = roiRest.shape[0]
    #print("roiRest_height:" + str(roiRest_height))
    
    grayRest = cv2.cvtColor(roiRest,cv2.COLOR_RGB2GRAY)
    _,thresheRst = cv2.threshold(grayRest, 100, 255, cv2.THRESH_BINARY_INV)
    blurred_image = cv2.GaussianBlur(thresheRst.copy(),(9,9),0)
    #canny = cv2.Canny(blurred_image,200,255)

    contoursRest, hierachy = cv2.findContours(blurred_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    AllDetectedCars = []
    

    for cntRest in contoursRest:
    
        #print(cv2.contourArea(cntRest))

        # Make sure the contour area is somewhat higher than some threshold to make sure its a car and not some noise.
        if cv2.contourArea(cntRest) > 500:
            #print(cv2.contourArea(cntRest))
            # Retrieve the bounding box coordinates from the contour.
            xcntRest, ycntRest, widthcntRest, heightcntRest = cv2.boundingRect(cntRest)
            
            #yAxisIsCaptured.append({'Y1': ycntRest, 'Y2': ycntRest+heightcntRest})
            AllDetectedCars.append([xcntRest, ycntRest, heightcntRest])


            #yCntl = yCntl + MyCarArea_Adujst_Height
            #xCnt = xCnt + MyCarArea_Adujst_Width
            
            # Draw a bounding box around the car.
            cv2.rectangle(roiRest, (xcntRest , ycntRest), (xcntRest + widthcntRest, ycntRest + heightcntRest),(0, 255, 0), 2)
            #roiCar = OriginalImage.copy()[yCntl:yCntl + heightCnt, xCnt:xCnt + widthCntl]

    # sort by X (The close one)
    from operator import itemgetter
    AllDetectedCars = sorted(AllDetectedCars, key=itemgetter(0))

    bestArea=0
    bestY1=myyCarPox 
    bestY2= myyCarPox + myheightCnt

    if len(AllDetectedCars) > 0 :

        closeCar= AllDetectedCars[0]

        #print(closeCar)



        area1 = closeCar[1]-0
        area2  = roiRest_height -  closeCar[1] + closeCar[2]
        #print("Area1 : " + str(area1) + " Area2:" + str(area2))

        if area1 > area2 :
            bestArea = area1
            bestY1=0
            bestY2=closeCar[1]
        else:
            bestArea = area2
            bestY1=closeCar[1] + closeCar[2]
            bestY2=roiRest_height

        #print("bestArea:",bestY1,bestY2)
               


    keyboard.press(Key.space)
    time.sleep(0.2)
    keyboard.release(Key.space)

    #check if the car show go up or down

    #print(yCntl,bestY2)

    carYposition = int((myyCarPox + myyCarPox + myheightCnt)/2)
    #ChosenFreeYposition = int((bestY1 + bestY2) /2) 

    #print("Car Yposition :" + str(carYposition)+ "  Best Area :   Y1:"+str(bestY1)+ " Y2: "+str(bestY2))

    safeParamter = 35
    pixelsForBrake = 300

    if carYposition-safeParamter > bestY1 and carYposition+safeParamter < bestY2 : 
        print(" -> Do nothing " + "Car Yposition :" + str(carYposition)+ "  Best Area : Y1:"+str(bestY1)+ " Y2: "+str(bestY2))

    elif carYposition + safeParamter > bestY2 and len(AllDetectedCars) > 0:
        print(" -> Go Up " + "Car Yposition :" + str(carYposition)+ "  Best Area : Y1:"+str(bestY1)+ " Y2: "+str(bestY2))
        if closeCar[0] - myxCarPox < pixelsForBrake :
            
            keyboard.press(Key.left)
            #print("brake inside up")
            time.sleep(0.5)
            keyboard.release(Key.left)
            keyboard.press(Key.space)
            time.sleep(1)
            keyboard.release(Key.space)
            keyboard.press(Key.up)
            time.sleep(1)
            keyboard.release(Key.up)
            print("Go Up ")
  
    elif carYposition - safeParamter < bestY1 and len(AllDetectedCars) > 0 :
        print(" -> Go Down " + "Car Yposition :" + str(carYposition)+ "  Best Area : Y1:"+str(bestY1)+ " Y2: "+str(bestY2))
        if closeCar[0] - myxCarPox < pixelsForBrake :
            keyboard.press(Key.left)
            time.sleep(0.5)
            keyboard.release(Key.left)
            keyboard.press(Key.space)
            time.sleep(1)
            keyboard.release(Key.space)
            keyboard.press(Key.down)
            time.sleep(1)
            keyboard.release(Key.down)
            print("Go Down ")

    if carYposition == 0:
        keyboard.press(Key.up)
        time.sleep(0.5)
        keyboard.release(Key.up)




    else:
        print("Do nothing")

 


    cv2.imshow("OriginalImage",OriginalImage)
    cv2.imshow("MyCarBlurred",MyCarBlurred)
    #cv2.imshow("blurred_image",blurred_image)
    cv2.imshow("roi",roi)
    cv2.imshow("roiCar",roiCar)

    cv2.imshow("roiRest",roiRest)
    cv2.imshow("blurred_image",blurred_image       )
    

    
       
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cv2.destroyAllWindows() 
