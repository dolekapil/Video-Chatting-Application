import socket

class SocketConnection:

    #Socket connection class is used to handle the sending and receiving of frames
    #between client and server.

    '''
    Init method will initialize the variables.
    '''
    def __init__(self, socket=None):
        if socket is None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.socket = socket

    #Connect method will establish connection with given
    #IP address and port number.
    def connection(self, host, port):
        self.socket.connect((host, port))

    #sendingFrame method will send the frames
    def sendingFrame(self, framestring):
        totalNumberOfFrameSend = 0
        numberOfFrameToBeSent = 0
        lengthOfEachFrame = len(framestring)
        lengthstr = str(lengthOfEachFrame).zfill(8)

        while numberOfFrameToBeSent < 8:
            #sending the frame. Encode method is used to convert the
            #string into bytes.
            numberOfFrameSent = self.socket.send((lengthstr[numberOfFrameToBeSent:]).encode())
            #handle the socket exception
            if numberOfFrameSent == 0:
                raise RuntimeError("connection lost")
            numberOfFrameToBeSent += numberOfFrameSent

        while totalNumberOfFrameSend < lengthOfEachFrame:
            numberOfFrameSent = self.socket.send(framestring[totalNumberOfFrameSend:])
            if numberOfFrameSent == 0:
                raise RuntimeError("connection lost")
            totalNumberOfFrameSend += numberOfFrameSent

    #receivingFrame will receive the frames and process it.
    def receivingFrame(self):
        totalFrameReceived = 0
        numberOfFrameReceived = 0
        frameListArray = []
        frameListTempArray = []
        while numberOfFrameReceived < 8:
            #Check for number of remaining frames
            remainingNumberOfFrames = self.socket.recv((8 - numberOfFrameReceived))
            #handling exception
            if remainingNumberOfFrames == '':
                raise RuntimeError("connection lost")
            frameListTempArray.append(remainingNumberOfFrames)
            numberOfFrameReceived += len(remainingNumberOfFrames)
        #here, b is used to convert the string into bytes
        lengthOfFrame = b''.join(frameListTempArray)
        length = int(lengthOfFrame)

        while totalFrameReceived < length:
            remainingNumberOfFrames = self.socket.recv(length - totalFrameReceived)
            if remainingNumberOfFrames == '':
                raise RuntimeError("Socket connection broken")
            frameListArray.append(remainingNumberOfFrames)
            totalFrameReceived += len(remainingNumberOfFrames)
        # here, b is used to convert the string into bytes
        return b''.join(frameListArray)
