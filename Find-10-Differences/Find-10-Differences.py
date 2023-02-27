import cv2
import numpy as np

img = cv2.imread("Open-CV/Find-10-Differences/two-images.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

_ , thresh = cv2.threshold(gray , 230, 255 , cv2.THRESH_BINARY_INV)

canny = cv2.Canny(thresh , 254 , 255)

# extract the two images 
contours , hierarchy = cv2.findContours(canny.copy() , cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#cv2.drawContours(img, contours, -1 , (0,255,0) ,2 )

# if the contours detected more than 2 area, we will grab the two biggest areas
sortedCon = sorted(contours, key = cv2.contourArea)

# area 1
x,y,w,h = cv2.boundingRect(sortedCon[0])
cv2.rectangle(img, (x,y), (x+w , y+h), (255,0,0), 3)

# get the first image
roi = img.copy()[y:y+h , x:x+w]

# area 2
x1,y1,w1,h1 = cv2.boundingRect(sortedCon[1])
cv2.rectangle(img, (x1,y1), (x1+w1 , y1+h1), (255,0,0), 3)
# get the second image
roi2 = img.copy()[y1:y1+h1 , x1:x1+w1]

# are the images the same size ?
print(roi.shape)
print(roi2.shape)

#(781, 1121, 3)
#(782, 1120, 3)

# adjust pixels since the shapes are not equal 
roi2H = roi2.shape[0]
print(roi2H)
roi2 = roi2[0:roi2H-1, :]
print(roi2.shape)

roi1W = roi.shape[1]
print(roi1W)
roi = roi[: , 0:roi1W-1]
print(roi.shape)


# same shape .

# calcultae the absolute difference between the two arrays

diff = 255 - cv2.absdiff(roi,roi2)

#let's create HSV mask

lower = np.array([0,0,0])
upper = np.array([180,255,255])

imgHSV = cv2.cvtColor(diff, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(imgHSV, lower, upper)

result = cv2.bitwise_and(diff, diff , mask=mask)

blur = cv2.GaussianBlur(result, (11,11), 0) # make blur to remoce noise
canny = cv2.Canny(blur, 50 , 150)
edges = cv2.dilate(canny, None)

contours , hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:

    # get the box coordinates
    x, y, width, height = cv2.boundingRect(cnt)

    # draw a bpx
    cv2.rectangle(result, (x,y), (x+width, y+height), (0,0,255), 2)
    cv2.rectangle(roi, (x,y), (x+width, y+height), (0,0,255), 2)
    cv2.rectangle(roi2, (x,y), (x+width, y+height), (0,0,255), 2)



cv2.imshow("result", result)



cv2.imshow("roi",roi)
cv2.imshow("roi2",roi2)



cv2.imshow("canny", canny)
cv2.imshow("edges", edges)
#cv2.imshow("trhesh", thresh)
#cv2.imshow("gray",gray)
#cv2.imshow("img",img)
cv2.waitKey(0)

#cv2.imwrite("c:/temp/roi.png", roi)
#cv2.imwrite("c:/temp/roi2.png", roi2)
#cv2.imwrite("c:/temp/canny.png", canny)
#cv2.imwrite("c:/temp/result.png", result)


cv2.destroyAllWindows()