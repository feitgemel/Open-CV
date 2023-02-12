import cv2
import numpy as np

img = cv2.imread("Open-CV/Image-Segmentation-using-Contour-Detection/beach-and-boats.jpeg")

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
_ , tresh = cv2.threshold(gray,np.mean(gray), 255, cv2.THRESH_BINARY_INV   )



# GET CONTOURS

contours , hierarchy = cv2.findContours(tresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

print(len(contours)) 

# lets get the bigger area

cnt = sorted(contours, key=cv2.contourArea)[-1]


mask = np.zeros( (750, 1038), dtype="uint8" )

maskedRed = cv2.drawContours(mask,[cnt] , -1 , (0 , 0 , 255), -1)
maskedFinal = cv2.drawContours(mask,[cnt] , -1 , (255 , 255 , 255), -1)

finalImage = cv2.bitwise_and(img, img, mask=maskedFinal)

cv2.imshow("Original", img)
cv2.imshow("maskedFinal", finalImage)

cv2.imwrite("c:/temp/maskedFinal.jpg",maskedFinal)
cv2.imwrite("c:/temp/finalImage.jpg",finalImage)

cv2.waitKey(0)

cv2.destroyAllWindows()