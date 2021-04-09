import cv2

img = cv2.imread('C:\Python Code\FacialDetection\Gal-Gadot-Wonder-Woman.gif')

cv2.imshow('img',img)

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

invertedImage = 255-gray

blurred = cv2.GaussianBlur(invertedImage,(21,21),0)

InvBlurred = invertedImage = 255-blurred

sketch = cv2.divide(gray,InvBlurred,scale = 256.0)

cv2.imwrite('C:\Python Code\FacialDetection\Gal-Gadot-Wonder-Woman-sketch.jpg',sketch)

cv2.imshow('sketch',sketch)
cv2.waitKey()