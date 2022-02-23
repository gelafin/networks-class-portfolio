# Author: Mark Mendez
# Date: 02/22/2022
# used starter code and concepts from "Computer Networking: A Top-Down Approach" by James F. Kurose and Keith Ross

from socket import *

PORT_NUMBER = 8011

# Configure server details necessary for connection.
serverName = 'localhost'  # server hostname or IP address
serverPort = PORT_NUMBER  # arbitrary port > 1023 (source: previous assignment instructions) matching server

# Choose a message to send to the server specified above
message = 'GET /imaginary-page.html HTTP/1.1\r\nHost:example.example\r\n\r\n'

# Create a client socket,
# using default address family (SOCK_STREAM means to use TCP)
client_socket = socket(family=AF_INET, type=SOCK_STREAM)

# Connect to the server specified above
client_socket.connect((serverName, serverPort))

# Send message to server
print(f'[client]\nRequest:\n{message}')
client_socket.send(message.encode())

# Receive first piece of response from server.
# Note from recv() docs:
# For best match with hardware and network realities,
# the value of bufsize should be a relatively small power of 2, for example, 4096
BUFFER_SIZE = 1024
raw_res = client_socket.recv(BUFFER_SIZE)

# Receive remaining pieces of response from server in a loop,
# to enable arbitrarily large files to be received.
# The server in this project will close the connection after sending its data,
# so detect when recv() returns <= 0 bytes. (source: assignment document)
# TODO: this loop condition could be updated to respect a protocol indicating message length
res_message = ''
while len(raw_res) > 0:
    # Decode raw byte response message,
    # then append this segment of the message
    res_message += raw_res.decode()

    # Receive next piece of the message or a bytes object of length 0
    raw_res = client_socket.recv(BUFFER_SIZE)

# Print server response
if res_message != '':
    print('[client]\n*received message*')
    print(f'\tlength: {len(res_message)}')
    print(res_message)

# Close socket connection
client_socket.close()
