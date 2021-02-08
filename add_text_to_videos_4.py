import cv2
import datetime


cap=cv2.VideoCapture(0) # try 0 or -1 for the connected camera index

cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

print('Is the video is opened ? : ')
print(cap.isOpened())

while (cap.isOpened()):
    ret,frame = cap.read()

    if ret == True:

        font = cv2.FONT_HERSHEY_SIMPLEX
        text='Width:'+str(cap.get(cv2.CAP_PROP_FRAME_WIDTH))+'      Height: '+str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 
        datet=str(datetime.datetime.now())

        frame = cv2.putText(frame,datet,(10,50),font,1,(0,255,255),2,cv2.LINE_AA)
        
        cv2.imshow('frame',frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()


