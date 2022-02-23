# Author: Mark Mendez
# Date: 02/22/2022
# used starter code and concepts from "Computer Networking: A Top-Down Approach" by James F. Kurose and Keith Ross

from socket import *

PORT_NUMBER = 8011

# Configure server details necessary for connection.
# This simple example only works with localhost.
serverName = 'localhost'  # server hostname or IP address
serverPort = PORT_NUMBER  # arbitrary port > 1023 (source: previous assignment instructions) matching client

# Choose a message to send to clients who connect
res_message = "HTTP/1.1 200 OK\r\n" \
              "Content-Type: text/html; charset=UTF-8\r\n\r\n" \
              "<html>Congratulations! You found me!</html>\r\n"

# Create a server socket,
# Using default address family (SOCK_STREAM means to use TCP)
server_socket = socket(family=AF_INET, type=SOCK_STREAM)

# Listen for connections
server_socket.bind(('', serverPort))
server_socket.listen(1)  # allow max of 1 queued connection

# Accept and handle requests
while True:
    # Accept a new connection
    connection_socket, client_address = server_socket.accept()

    # Decode raw byte response message,
    # then append this segment of the message.
    # Note from recv() docs:
    # For best match with hardware and network realities,
    # the value of bufsize should be a relatively small power of 2, for example, 4096
    BUFFER_SIZE = 1024
    req_message_raw = connection_socket.recv(BUFFER_SIZE).decode()

    # Print this socket's new request
    print(f'[server]\nConnected by {serverName}:{serverPort}')
    print(f'\n[server]\nReceived: {req_message_raw}')
    print(f'\n[server]\nSending response: {res_message}')

    # Send the response message
    connection_socket.send(res_message.encode())

    # Close the connection
    connection_socket.close()
