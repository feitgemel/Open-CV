import cv2

img = cv2.imread("Open-CV/Coin-Edge-Detection/coins.jpg")

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (7,7), 0)
canny = cv2.Canny(blur , 90, 255)

# lets find each coin by its contour
 
contours , hierarchy = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#cv2.drawContours(img, contours, -1 , (0,255,0), 2)

sortedCon = sorted(contours, key=cv2.contourArea)


# loop inside the sorted contours
for i , cont in enumerate(sortedCon):
    x, y, w, h = cv2.boundingRect(cont)
    print(i)
    #print(x, y, w, h)

    # find the center of each circle
    X = x + int(w/2)
    Y = y + int(h/2)

    img = cv2.circle(img, (X,Y), 50 , (0,255,0), 2)

    img = cv2.putText(img = img , text=str(i), org=(X,Y), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1.0 , color=(0,255,255), thickness=2)


cv2.imshow("original image", img)
#cv2.imshow("gray", gray)
cv2.imshow("canny", canny)
cv2.waitKey(0)

cv2.imwrite("c:/temp/1.png",img)

cv2.destroyAllWindows()