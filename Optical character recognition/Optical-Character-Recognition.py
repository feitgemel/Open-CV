import cv2 
import matplotlib.pyplot as plt 
import easyocr 

path = "Open-CV/Optical character recognition/sign.jpg"
img = cv2.imread(path)

# create detector
reader = easyocr.Reader(['en'])

# detect text on the image
myText = reader.readtext(img)
print(myText)

minThresholdForDisplay = 0.25

for numerator , detectedText in enumerate(myText):
    print(detectedText)

    bbox , text , score = detectedText
    pos1 = bbox[0]
    pos2 = bbox[2]

    if score > minThresholdForDisplay :
        cv2.rectangle(img,pos1,pos2, (0,0,0), 5)
        cv2.putText(img,text,pos1,cv2.FONT_HERSHEY_PLAIN, 5, (255,0,0), 5)


cv2.imwrite("c:/temp/opticalRecog.png",img)
plt.imshow(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
plt.show()
