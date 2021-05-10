import cv2

cap = cv2.VideoCapture(0)

# You can update your camera resolution
cap.set(3,1920)
cap.set(4,1080)

while cap.isOpened():

    re, frame = cap.read()

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    invertImage = 255-gray
    blurred = cv2.GaussianBlur(invertImage,(21,21),0)
    invBlurred = 255-blurred

    sketch = cv2.divide(gray,invBlurred,scale = 256.0)

    
    cv2.imshow('frame',frame)
    cv2.imshow('sketch',sketch)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()