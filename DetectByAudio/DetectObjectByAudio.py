import cv2
import pandas as pd
import sounddevice as sd # for the record
from scipy.io.wavfile import write # to save the file
import numpy as np
import soundfile # for converting the audio format
import speech_recognition as sr # for speech to text



# load the model 
net = cv2.dnn.readNet("C:/GitHub/Open-CV/DetectByAudio/yolov4-tiny.weights","C:/GitHub/Open-CV/DetectByAudio/yolov4-tiny.cfg")
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(416,416), scale= 1/255)


# load the classes names and store in a list

classesNames = []
df = pd.read_csv("DetectByAudio/classes.txt", header=None, names=["ClassName"])
for index , row in df.iterrows():
    ClassName = df.iloc[index]['ClassName']
    classesNames.append(ClassName)

#print(classesNames)


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

# button dims
x1 = 20
y1 = 20
x2 = 570
y2 = 90

fs = 44100 # audio rate
secods = 3 # duration
audioFileName = "c:/temp/output.wav"

ButtonFlag = False
LookForThisClassName = ""

# capture the mouse , get the lift click and record audio
def recordAudioByMouseClick(event , x, y, flags, params):

    global ButtonFlag
    global LookForThisClassName

    if event == cv2.EVENT_LBUTTONDOWN:
        #print(x,y)
        if x1<= x <= x2 and y1<= y <= y2 :
            print("Click inside the button")

            # record a voice for 3 seconds
            myrecording = sd.rec(int(secods*fs), samplerate=fs, channels=2)
            sd.wait() # wait until the recording is finished
            write(audioFileName, fs, myrecording) # save the audio file
            
            # extract the text from an audio
            LookForThisClassName = getTextFromAudio()


            if ButtonFlag is False:
                ButtonFlag = True

        else :
            print("Click outside the button")
            ButtonFlag = False



def getTextFromAudio():

    #convert the audio file for Google API
    data , samplerate = soundfile.read(audioFileName)
    soundfile.write('c:/temp/outputNew.wav', data , samplerate, subtype='PCM_16')

    # extract the text
    recognizer = sr.Recognizer()
    jackhammer = sr.AudioFile('c:/temp/outputNew.wav')

    with jackhammer as source:
        audio = recognizer.record(source)
    
    result = recognizer.recognize_google(audio)

    print(result)
    return result



# create our window
cv2.namedWindow("Frame") # set the same name
cv2.setMouseCallback("Frame",recordAudioByMouseClick ) 
 

while True:
    rtn , frame = cap.read()

    # Detect objects
    (class_ids,scores,bboxes) = model.detect(frame)
    #print ("Class ids:", class_ids)
    #print ("Scores :", scores)
    #print ("Bboxes :", bboxes)

    for class_id , score , bbox in zip(class_ids, scores, bboxes):
        # draw a rectangle for each detected object
        x , y, width , height = bbox # x, y is the left upper corner
        #print (x , y, width , height )
        name = classesNames[class_id]

        index = LookForThisClassName.find(name) # look for the text inside a sring

        if ButtonFlag is True and index > 0 :

            cv2.rectangle(frame, (x,y) , (x+width, y +height), (130,50,50), 3)
            cv2.putText(frame, name , (x, y-10), cv2.FONT_HERSHEY_COMPLEX, 1 , (120,50,50), 2)

    # draw a "Button"
    cv2.rectangle(frame , (x1,y1),(x2,y2), (153,0,0), -1 ) #-1 is filled cretangle
    cv2.putText(frame , "Click for record - 3 seconds", (40,60) , cv2.FONT_HERSHEY_COMPLEX, 1 , (255,255,255), 2) #white color

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

