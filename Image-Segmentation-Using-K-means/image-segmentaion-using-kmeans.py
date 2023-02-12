import cv2
import numpy as np

img = cv2.imread("Open-CV/Image-Segmentation-Using-K-means/beach-and-boats.jpeg")

print(img.shape)

# reshape the image to two dim
twoDim = img.reshape((-1,3))
print(twoDim.shape)

# convert it to float 
twoDim = np.float32(twoDim)

# k -> defines the clustering (grouping) of the pixels

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER , 10 , 1.0)
K=3

attamps = 10

ret , label , center = cv2.kmeans(twoDim, K, None , criteria , attamps, cv2.KMEANS_PP_CENTERS)
center = np.uint8(center)

res = center[label.flatten()]
result_image = res.reshape((img.shape))

cv2.imshow("result_image",result_image)

cv2.imwrite("c:/temp/result3-100.jpg",result_image)






cv2.imshow("img",img)
cv2.waitKey(0)

cv2.destroyAllWindows()