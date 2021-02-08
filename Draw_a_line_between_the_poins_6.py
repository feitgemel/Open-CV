import numpy as np  
import cv2

#events = [i for i in dir(cv2) if 'EVENT' in i] #get all the events names in the cv2
#print(events)

def click_event(event,x,y,flags,param): # event click in the mouse and x and y that was clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img,(x,y),3,(0,0,255),-1)
        points.append((x,y))
        if len (points) >=2: # if there more the 2 points we need to create lines
            cv2.line(img,points[-1],points[-2],(255,0,0),5)  # points[-1] means the last x,y in the array

        cv2.imshow('image',img)

    


img = np.zeros([512,512,3],np.uint8) # black image
#img=cv2.imread('lena.jpg',1)
points=[]
cv2.imshow('image',img)
cv2.setMouseCallback('image',click_event)
cv2.waitKey(0)
cv2.destroyAllWindows
