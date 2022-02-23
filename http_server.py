# Author: Mark Mendez
# Date: 01/09/2022
# used starter code and concepts from "Computer Networking: A Top-Down Approach" by James F. Kurose and Keith Ross

from socket import *

# configure server details necessary for connection
# this simple example only works with localhost
serverName = 'localhost'  # server hostname or IP address
serverPort = 8011  # arbitrary port > 1023 (source: previous assignment instructions)

# choose a message to send to clients who connect
res_message = "HTTP/1.1 200 OK\r\n" \
              "Content-Type: text/html; charset=UTF-8\r\n\r\n" \
              "<html>Congratulations! You've downloaded the first Wireshark lab file!</html>\r\n"

# create a server socket,
# using default address family (SOCK_STREAM means to use TCP)
server_socket = socket(family=AF_INET, type=SOCK_STREAM)

# listen for connections
server_socket.bind(('', serverPort))
server_socket.listen(1)  # allow max of 1 queued connection

# accept and handle requests
while True:
    connection_socket, addr = server_socket.accept()
    # Remember to decode raw byte response message,
    # then append this segment of the message.
    # Note from recv() docs:
    # For best match with hardware and network realities,
    # the value of bufsize should be a relatively small power of 2, for example, 4096
    req_message_raw = connection_socket.recv(1024).decode()

    # print this socket's new request
    print('Connected by ', '(', serverName, ',', serverPort, ')')
    print('\nReceived:', req_message_raw)
    print('\nSending>>>>>>>', res_message, '\n<<<<<<<')

    # send the response message
    connection_socket.send(res_message.encode())

    # close the connection
    connection_socket.close()
