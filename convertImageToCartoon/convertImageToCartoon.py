import cv2

# choose an image
# You can find the demo images in the Gihub repo.
img = cv2.imread('C:\Python-Code\convertImagetoSketch\Gal-Gadot-Wonder-Woman.gif')

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
invertedImage = 255-gray

blurred = cv2.GaussianBlur(invertedImage,(21,21),0)
invBlurred = 255 - blurred

sketch = cv2.divide(gray,invBlurred,scale = 256.0)

# save the image
cv2.imwrite('C:\Python-Code\convertImagetoSketch\Gal-Gadot-Wonder-Woman-sketch.jpg')

cv2.imshow('img',img)
cv2.imshow('sketch',sketch)

cv2.waitKey()


