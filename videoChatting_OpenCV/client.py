import sys
import socket
import SocketConnection
from io import StringIO
from videoStreaming import Streaming
import pyaudio
from threading import Thread

class Client:
    #Client class is used to establish the TCP connection
    #with server

    '''
        Init method will create the socket for client and will establish
        connection with server.
    '''

    def __init__(self, ipAddress = "localhost"):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((ipAddress, 4000))
        self.videoSocket = SocketConnection.SocketConnection (self.clientSocket)
        print("client started")
        self.videoStreaming = Streaming(1,"client",1)
        self.input = StringIO()

    #TCPConnection method will establish the connection of client
    #with server.
    def TCPConnection(self):
        #run the while loop continuously
        while True:
            #get the frame from video streaming class
            frame=self.videoStreaming.getTheFrame()
            #send the frame to the server
            self.videoSocket.sendingFrame(frame)
            frame = self.videoSocket.receivingFrame()
            self.videoStreaming.setTheFrame(frame)

# Method for receiving audio stream data.
def receiveAudio():
    # We are using pyAudio library.
    pAudio = pyaudio.PyAudio()
    receiveStream = pAudio.open(format=pAudio.get_format_from_width(2), channels=1, rate=44100, output=True,
                    frames_per_buffer=1024)
    # Establishing socket connection for getting audio data.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 8081))
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
    sock.connect((ipAddress, 8080))

    sendFrames = []
    # sending stream data.
    while True:
        sendData = sendStream.read(1024)
        sendFrames.append(sendData)
        sock.sendall(sendData)

# Method for sending video threads
def sendVideo():
    #calling the constructor
    clientObject = Client(ipAddress)
    clientObject.TCPConnection()	
	
		
if __name__ == "__main__":
    #default ip address is set to localhost
    ipAddress = "localhost"
    #check if user has provided the ip address
    #in the command line itself
    if len(sys.argv) == 2:
        ipAddress = sys.argv[1]

    print ("Client is trying to establish connection with " + ipAddress)
    videoThread = Thread(target=sendVideo)
    videoThread.start()
    #Calling send and receive audio methods.
    sendThread = Thread(target = sendAudio,args=(ipAddress,))
    sendThread.start()
    receiveThread = Thread(target=receiveAudio)
    receiveThread.start()