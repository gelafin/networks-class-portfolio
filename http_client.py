# Author: Mark Mendez
# Date: 01/09/2022
# used starter code and concepts from "Computer Networking: A Top-Down Approach" by James F. Kurose and Keith Ross

from socket import *


# configure server details necessary for connection
serverName = 'gaia.cs.umass.edu'  # server hostname or IP address
serverPort = 80  # standard Web port

# choose a message to send to the server specified above
message = 'GET /wireshark-labs/HTTP-wireshark-file3.html HTTP/1.1\r\nHost:gaia.cs.umass.edu\r\n\r\n'

# create a client socket,
# using default address family (SOCK_STREAM means to use TCP)
client_socket = socket(family=AF_INET, type=SOCK_STREAM)

# connect to the server specified above
client_socket.connect((serverName, serverPort))

# send message to server
print('Request: ' + message)
client_socket.send(message.encode())

# receive first piece of response from server
# Note from recv() docs:
# For best match with hardware and network realities,
# the value of bufsize should be a relatively small power of 2, for example, 4096
raw_res = client_socket.recv(1024)

# Receive remaining pieces of response from server in a loop,
# to enable arbitrarily large files to be received.
# The gaia.cs.umass.edu server will close the connection after sending its data,
# so detect when recv() returns <= 0 bytes. (source: assignment document)
res_message = ''
while len(raw_res) > 0:
    # remember to decode raw byte response message,
    # then append this segment of the message
    res_message += raw_res.decode()

    # receive next segment of the message or a bytes object of length 0
    raw_res = client_socket.recv(1024)

# print server response
if res_message != '':
    print('[RECV] - length:', len(res_message))
    print(res_message)

# close socket connection
client_socket.close()
