import socket
import SocketConnection
from videoStreaming import Streaming
import pyaudio
from threading import Thread
import sys

class Server:
    #server class will establish the connection client

    '''
        Init method will initialize the variables of server class.
    '''
    def __init__(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind(("", 4000))
        self.serverSocket.listen(5)
        self.videoStreaming = Streaming(1,"server",1)
        print("server started")
        print ("Server is listening for connection on port 4000")

    #This method will handle the server connection with client
    def TCPConnection(self):
        #while loop will run continuously
        while True:
            #accept the connection with client
            clientSocket, ipAddress = self.serverSocket.accept()
            print ("Server established connection with client : ", ipAddress)
            videoSocket = SocketConnection.SocketConnection(clientSocket)
            while True:
                #received the frame from client
                frame=videoSocket.receivingFrame()
                self.videoStreaming.setTheFrame(frame)
                frame=self.videoStreaming.getTheFrame()
                #sent the frame to client
                videoSocket.sendingFrame(frame)

# Method for receiving audio stream data.
def receiveAudio():
    # We are using pyAudio library.
    pAudio = pyaudio.PyAudio()
    receiveStream = pAudio.open(format=pAudio.get_format_from_width(2), channels=1, rate=44100, output=True,
                    frames_per_buffer=1024)
    # Establishing socket connection for getting audio data.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 8080))
    sock.listen(1)
    connections, address = sock.accept()
    print('Connection established with host for audio data: ', address)
    receiveData = connections.recv(1024)

    receiveFrames = []
    # Receiving stream data.
    while True:
        receiveStream.write(receiveData)
        receiveData = connections.recv(1024)
        receiveFrames.append(receiveData)

# Method for send audio stream data.
def sendAudio(ipAddress):
    # We are using pyAudio library for audio data.
    pAudio = pyaudio.PyAudio()
    sendStream = pAudio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    # Establishing socket connection for sending audio data.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ipAddress, 8081))

    sendFrames = []
    # sending stream data.
    while True:
        sendData = sendStream.read(1024)
        sendFrames.append(sendData)
        sock.sendall(sendData)

# Method for sending video frames.
def sendVideo():
    #creating the object of server class
    serverObject = Server()
    serverObject.TCPConnection()


if __name__ == "__main__":
    #default ip address is set to localhost
    ipAddress = "localhost"
    #check if user has provided the ip address
    #in the command line itself
    if len(sys.argv) == 2:
        ipAddress = sys.argv[1]

    # Calling video thread.
    videoThread = Thread(target=sendVideo)
    videoThread.start()
    #Calling send and receive audio methods.
    sendThread = Thread(target = sendAudio,args=(ipAddress,))
    sendThread.start()
    receiveThread = Thread(target=receiveAudio)
    receiveThread.start()