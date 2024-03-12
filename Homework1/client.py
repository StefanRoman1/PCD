import random
import socket
import time
import argparse

localhost = "127.0.0.1"
port = 1512


def tcp_streaming(message_size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (localhost, port)
    sock.connect(server_address)

    start_time = time.time()

    message_size = int(message_size)

    bytes_sent = 0
    number_of_messages = 0

    while bytes_sent < message_size:
        curr_message_size = random.randint(1, 65000)
        message = b'0' * curr_message_size
        sock.send(curr_message_size.to_bytes(8, byteorder='big'))
        sock.send(message)
        bytes_sent += curr_message_size
        number_of_messages += 1

    end_time = time.time()
    total_time = end_time - start_time

    print(f"Total transfer time: {total_time:.3f} seconds")
    print(f"Number of messages sent : {number_of_messages}")
    print(f"Number of bytes sent : {bytes_sent}")

    sock.close()


def tcp_stop_and_wait(message_size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (localhost, port)
    sock.connect(server_address)

    start_time = time.time()

    message_size = int(message_size)

    bytes_sent = 0
    number_of_messages = 0

    while bytes_sent < message_size:
        curr_message_size = random.randint(1, 65000)
        message = b'0' * curr_message_size
        sock.send(curr_message_size.to_bytes(8, byteorder='big'))
        sock.send(message)

        response = sock.recv(3)
        if response.decode() == "ACK":
            bytes_sent += curr_message_size
            number_of_messages += 1

    end_time = time.time()
    total_time = end_time - start_time

    print(f"Total transfer time : {total_time:.3f} seconds")
    print(f"Number of messages sent: {number_of_messages}")
    print(f"Number of bytes sent: {bytes_sent}")

    sock.close()


def udp_streaming(message_size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (localhost, port)

    start_time = time.time()

    message_size = int(message_size)

    bytes_sent = 0
    number_of_messages = 0

    while bytes_sent < message_size:
        curr_message_size = random.randint(1, 65000)
        message = b'0' * curr_message_size
        sock.sendto(message, server_address)
        bytes_sent += curr_message_size
        number_of_messages += 1

    end_time = time.time()
    total_time = end_time - start_time
    sock.sendto(b'', server_address)

    print(f"Transfer time : {total_time:.3f} seconds")
    print(f"Number of messages sent : {number_of_messages}")
    print(f"Number of bytes sent : {bytes_sent}")

    sock.close()


def udp_stop_and_wait(message_size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (localhost, port)

    start_time = time.time()

    bytes_sent = 0
    number_of_messages = 0

    while bytes_sent < message_size:
        curr_message_size = random.randint(1, 65000)
        message = b'0' * curr_message_size
        sock.sendto(message, server_address)

        response, server_address = sock.recvfrom(3)
        if response.decode() == "ACK":
            bytes_sent += curr_message_size
            number_of_messages += 1

    sock.sendto(b'', server_address)

    end_time = time.time()
    total_time = end_time - start_time

    print(f"Transfer time : {total_time:.3f} seconds")
    print(f"Number of messages sent : {number_of_messages}")
    print(f"Number of bytes sent : {bytes_sent}")

    sock.close()


parser = argparse.ArgumentParser(description='TCP/UDP Client')
parser.add_argument('-c', '--connection', type=str,
                    choices=['TCP', 'UDP'], required=True, help='connection type: TCP or UDP')
parser.add_argument('-t', '--transfer_mode', type=str, choices=[
    'streaming', 'stop-and-wait'], required=True, help='transfer mechanism: streaming or stop-and-wait')
parser.add_argument('-size', '--size_message', type=str, choices=[
    '500', '1000'], required=True, help='sent data size in MB')

args = parser.parse_args()

if args.connection.upper() == "TCP":
    if args.transfer_mode.lower() == "streaming":
        tcp_streaming(int(args.size_message) * 1024 * 1024)
    elif args.transfer_mode.lower() == "stop-and-wait":
        tcp_stop_and_wait(int(args.size_message) * 1024 * 1024)
    else:
        print("Transfer mechanism not supported")
        exit(0)
elif args.connection.upper() == "UDP":
    if args.transfer_mode.lower() == "streaming":
        udp_streaming(int(args.size_message) * 1024 * 1024)
    elif args.transfer_mode.lower() == "stop-and-wait":
        udp_stop_and_wait(int(args.size_message) * 1024 * 1024)
    else:
        print("Transfer mechanism not supported")
        exit(0)
else:
    print("Protocol not supported")
    exit(0)
