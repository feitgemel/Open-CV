import numpy as np  
import cv2

#events = [i for i in dir(cv2) if 'EVENT' in i] #get all the events names in the cv2
#print(events)

def click_event(event,x,y,flags,param): # event click in the mouse and x and y that was clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        blue =  img[y,x,0]
        green = img[y,x,1]
        red=    img[y,x,2]
        cv2.circle(img,(x,y),3,(0,0,255),-1) # draw a point
        
        # build the new window
        mycolorImage = np.zeros([512,512,3],np.uint8) # create a black image
        # now we will fill the image
        mycolorImage[:]=[blue,green,red]
        cv2.imshow('color',mycolorImage)

        # the main image 
        cv2.imshow('image',img)

    


#img = np.zeros([512,512,3],np.uint8) # black image
img=cv2.imread('lena.jpg',1)
points=[]
cv2.imshow('image',img)
cv2.setMouseCallback('image',click_event)
cv2.waitKey(0)
cv2.destroyAllWindows
