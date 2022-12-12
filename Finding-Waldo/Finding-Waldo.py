import cv2

image = cv2.imread("Finding-Waldo\WaldoBeach.jpg")
waldo = cv2.imread("Finding-Waldo\waldo.jpg",0) # load it as gray scale

# convert the image to gray scale
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

# find one image inside another image
result = cv2.matchTemplate(gray, waldo , cv2.TM_CCOEFF)
min_val , max_val , min_loc , max_loc = cv2.minMaxLoc(result)

# this is the left position of Waldo

print (max_loc)

top_left = max_loc
bottom_right = (top_left[0] + 50 , top_left[1] + 50 )

# lets show the position 
#cv2.circle (image, max_loc , 10 , (255,0,0), 2)
cv2.rectangle(image, top_left, bottom_right, (255,0,0), 5)

cv2.imshow("img", image)
#cv2.imshow("waldo", waldo)
cv2.waitKey(0)

cv2.imwrite("Finding-Waldo\WaldoBeach2.jpg",image)

cv2.destroyAllWindows()