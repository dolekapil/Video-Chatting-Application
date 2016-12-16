import io
import numpy
import cv2
from PIL import Image

#Streaming class will create the frame to be send and will process
#the frame received
class Streaming:
    '''
        Init method will initialize the variables of streaming class.
    '''
    def __init__(self,mode=1,name="w1",frameCaptured=1):

        self.indexOfCamera = 0
        self.name = name
        if frameCaptured == 1:
            self.webCam = cv2.VideoCapture(self.indexOfCamera)

    #This method will get the frames from the camera feed.
    def getTheFrame(self):
        valueReceived, image = self.webCam.read()
        count = cv2.waitKey(1)
        if (count == "n"):
            #get the frame from next camera index
            self.indexOfCamera += 1
            self.webCam = cv2.VideoCapture(self.indexOfCamera)
            if not self.webCam:
                #if next feed is not available then reset it to 0
                self.indexOfCamera = 0
                self.webCam = cv2.VideoCapture(self.indexOfCamera)

        getTheImageFromCV2 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        saveTheImageReceived = Image.fromarray(getTheImageFromCV2)
        bytesArray = io.BytesIO()
        saveTheImageReceived.save(bytesArray, 'jpeg')
        imageInBytes = bytesArray.getvalue()
        return imageInBytes

    #This method will set the value of frame received.
    def setTheFrame(self, frame_bytes):
        imageBytes = io.BytesIO(frame_bytes)
        setTheImage = Image.open(imageBytes)
        imageCV2 = cv2.cvtColor(numpy.array(setTheImage), cv2.COLOR_RGB2BGR)
        cv2.imshow(self.name, imageCV2)

if __name__=="__main__":
    streaming = Streaming(1,"streaming",1)
    while True:
        frame = streaming.getTheFrame()
        streaming.setTheFrame(frame)
