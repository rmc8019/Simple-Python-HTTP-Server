#import socket module
from socket import *
import sys # In order to terminate the program

def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)

    #Prepare a sever socket
    try:
        serverSocket.bind(('', port))
    except socket.error:
        serverSocket.close()
        serverSocket.bind(('', port))
    serverSocket.listen(1)

    while True:
        #Establish the connection
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()
        try:
            message = connectionSocket.recv(1024).decode()
            filename = message.split()[1]
            f = open(filename[1:])
            outputdata = f.read()

            #Send one HTTP header line into socket
            connectionSocket.send(('HTTP/1.1 200 OK\r\n').encode())
            connectionSocket.send(("Content-Type: text/html\r\n\r\n").encode())

            #Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())

            connectionSocket.send("\r\n".encode())
            connectionSocket.close()
            
        except IOError:
            #Send response message for file not found (404)
            if filename[1:] != "HelloWorld.html":
                connectionSocket.send(('HTTP/1.1 404 Not Found\r\n').encode())
                connectionSocket.send(("Content-Type: text/html\r\n\r\n").encode())
                connectionSocket.send(("<html><head>404 Not Found</head></html>\r\n\r\n").encode())

            #Close client socket
            connectionSocket.close()
            
    serverSocket.close()
    sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
    webServer(13331)
