# Author: Mark Mendez
# Date: 02/23/2022

from socket import socket
from socket_constants import *
from math import ceil


def send_message(outgoing_message: str, connection_socket: socket):
    """
    Sends a given message through a given socket,
    Segmenting data to respect window size (known through a constant global buffer size).
    Segmentation is done according to the made-up GELA372 protocol.
    In GELA372, the first byte of every packet is a "last packet" flag,
    and a receiver accumulates packets until detecting a flag of 1.
    :param outgoing_message: message to send to the other host
    :param connection_socket: socket object representing the connection
    """
    # Determine number of packets
    # (sacrificing the first byte of each packet to the "last packet" flag
    # and rounding up because there are no partial packets).
    payload_size = BUFFER_SIZE - 1
    packet_count = ceil(len(outgoing_message) / payload_size)

    # Send all but the last packet
    for packet_index in range(packet_count - 1):
        # Use the first packet byte for the flag, which is 0 in this loop
        last_packet_flag = GELA372_LAST_PACKET_FALSE

        # Get the next segment of the message
        slice_start = packet_index * payload_size
        slice_end = slice_start + payload_size
        message_payload = outgoing_message[slice_start:slice_end]

        # Assemble the packet in GELA372 format
        packet_raw_string = last_packet_flag + message_payload

        # Send this packet
        connection_socket.send(packet_raw_string.encode())

    # Send the last packet, with the "last packet" flag set
    last_packet_flag = GELA372_LAST_PACKET_TRUE
    message_payload = outgoing_message[-payload_size:len(outgoing_message)]
    packet_raw_string = last_packet_flag + message_payload
    connection_socket.send(packet_raw_string.encode())

    # print(f'DEBUG: sent whole message: {packet_raw_string}')


def receive_next_packet(connection_socket: socket) -> dict:
    """
    Receives the next packet of data from the given socket
    and parses the data according to the made-up GELA372 protocol.
    In GELA372, the first byte of every packet is a "last packet" flag,
    and a receiver accumulates packets until detecting a flag of 1.
    :param connection_socket: socket object representing the connection
    :return: packet data in the form
             {'is_last_packet': bool, 'payload': str}
    """
    # Receive a packet of raw byte message and decode it into a string
    incoming_message_packet = connection_socket.recv(BUFFER_SIZE).decode()
    # print(f'DEBUG: received whole message: {incoming_message_packet}')

    # Check last packet flag using the GELA372 protocol.
    last_packet_flag = incoming_message_packet[0:1]

    if last_packet_flag != GELA372_LAST_PACKET_FALSE and last_packet_flag != GELA372_LAST_PACKET_TRUE:
        raise Exception('received invalid packet flag')

    packet_payload = incoming_message_packet[1:len(incoming_message_packet)]
    is_last_packet = True if last_packet_flag == GELA372_LAST_PACKET_TRUE else False

    # Wrap up the extracted data, nice and neat
    packet_data_out = {
        'is_last_packet': is_last_packet,
        'payload': packet_payload
    }

    return packet_data_out
