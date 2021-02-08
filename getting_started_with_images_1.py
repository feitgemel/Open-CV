import cv2

print (cv2.__version__)
# img = cv2.imread('lena.jpg',0) # load the image in gray scale 
#img = cv2.imread('lena.jpg',1) # load the image in color scale 
img = cv2.imread('lena.jpg',-1)

print(img)

cv2.imshow('image',img)
k = cv2.waitKey(0) # 5 seconds

if k==27 : # ESC key
    cv2.destroyAllWindows()
elif k == ord('s'):
    cv2.imwrite('lena_copy.png',img)
    cv2.destroyAllWindows()

    