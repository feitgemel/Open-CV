import cv2
import numpy as np

OriginalImage = cv2.imread("Restore-Damaged-Photo/abraham.jpg")
cv2.imshow("Origina lImage",OriginalImage)

makredDamages = cv2.imread("Restore-Damaged-Photo/mask.jpg",0) # gray scale
cv2.imshow("makred Damages",makredDamages)

# lets create a mask with threshhold
ret , thresh = cv2.threshold(makredDamages, 254, 255 , cv2.THRESH_BINARY)
cv2.imshow("mask threshold",thresh)

# lets make the lines thicker
kernel = np.ones((7,7), np.uint8)
mask = cv2.dilate(thresh , kernel , iterations=1)
cv2.imshow("mask", mask)

# lets restore the image
restoredImage = cv2.inpaint(OriginalImage , mask , 3, cv2.INPAINT_TELEA)
cv2.imshow("restored Image", restoredImage) 
cv2.imwrite("Restore-Damaged-Photo/RestoredAbraham.jpg",restoredImage)

cv2.waitKey(0)







cv2.destroyAllWindows()