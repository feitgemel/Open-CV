import cv2
import numpy as np

img = cv2.imread('Open-CV/Words-Segmentation/book2.jpg')


def thresholding(image):
    img_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    # We need the words in white 
    ret, thresh = cv2.threshold(img_gray, 170, 255 , cv2.THRESH_BINARY_INV)
    
    # wee need the "merge" the characters to a single "words"
    thresh = cv2.GaussianBlur(thresh, (11,11), 0)
    ret, thresh = cv2.threshold(thresh, 130 , 255 , cv2.THRESH_BINARY)
    return thresh


thresh_img = thresholding(img)
cv2.imshow("thresh_img",thresh_img)


# line sementation

linesArray = []
kernelRows = np.ones((5,40), np.uint8)

# We will use dilation for the line sementation
dilated = cv2.dilate(thresh_img, kernelRows, iterations=1)
cv2.imshow("dilated",dilated)

# find contours
(contoursRows , heirarchy) = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#cv2.drawContours(img, contoursRows, -1 , (0,255,0), 2) # draw the contour around each row on the original image

# loop inside the contours and draw rectangle
for row in contoursRows :
    area = cv2.contourArea(row)
    if area > 500 :
        x , y, w, h = cv2.boundingRect(row)
        #cv2.rectangle(img, (x,y), (x+w, y+h), (40,100,250), 2)
        linesArray.append([x , y, w, h])

print(len(linesArray)) # 33 lines

# lets sort the line by the y position (from up to down)
sortedLinesArray = sorted(linesArray, key=lambda line : line [1])


# words segmentation

words = []
lineNumber = 0
all = []

# kernel for words
kernelWords = np.ones((7,7), np.uint8)
dilateWordsImg = cv2.dilate(thresh_img, kernelWords, iterations=1)
cv2.imshow("dilate Words Img",dilateWordsImg)

for line in sortedLinesArray :

    x,y,w,h = line

    roi_line = dilateWordsImg[y: y+h , x:x+w]
    #cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0),2 )
    (contoursWords , heirarchy) = cv2.findContours(roi_line.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for word in contoursWords:
        x1,y1,w1,h1 = cv2.boundingRect(word)
        cv2.rectangle(img,(x+x1,y+y1),(x+x1+w1,y+y1+h1),(255,255,0),2) 
        words.append([x+x1,y+y1,x+x1+w1,y+y1+h1])

    # sort the words by the X position
    sortedWords = sorted(words, key=lambda line : line[0]) #(x,y,w,h)

    # build a full array of lines and words

    for word in sortedWords:
        a = (lineNumber,word)
        all.append(a)

    lineNumber = lineNumber + 1

#print(all)

# show the first word in the first row
chooseWord = all[3][1]
print(chooseWord)

roiWord = img[chooseWord[1]:chooseWord[3], chooseWord[0]:chooseWord[2]]
cv2.imshow("Show a word", roiWord)


cv2.imshow("Show the words",img)
cv2.imwrite("c:/temp/segmentedBook.png",img)
cv2.waitKey(0)
cv2.destroyAllWindows()

