import socket
import argparse

localhost = "127.0.0.1"
port = 1512


def tcp_streaming():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (localhost, port)
    sock.bind(server_address)

    sock.listen(1)

    print(f"TCP-streaming listening on {localhost} : {port}")

    connection, client_address = sock.accept()

    bytes_read = 0
    messages_read = 0

    while True:
        message_size = int.from_bytes(connection.recv(8), byteorder='big')
        message = connection.recv(message_size)
        if not message:
            break
        bytes_read += len(message)
        messages_read += 1

    print(f"Used protocol : {args.connection.upper()}")
    print(f"Number of messages read: {messages_read}")
    print(f"Number of bytes read: {bytes_read}")

    connection.close()
    sock.close()


def tcp_stop_and_wait():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (localhost, port)
    sock.bind(server_address)

    sock.listen(1)

    print(f"TCP-stop-and-wait listening on {localhost} : {port}")

    connection, client_address = sock.accept()

    bytes_read = 0
    messages_read = 0

    while True:
        message_size = int.from_bytes(connection.recv(8), byteorder='big')
        message = connection.recv(message_size)
        if not message:
            break

        bytes_read += len(message)
        messages_read += 1

        response = b'ACK'
        connection.send(response)

    print(f"Used protocol : {args.connection.upper()}")
    print(f"Number of messages read : {messages_read}")
    print(f"Number of bytes read : {bytes_read}")

    connection.close()
    sock.close()


def udp_streaming():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (localhost, port)
    sock.bind(server_address)

    print(f"UDP-streaming listening on {localhost} : {port}")

    bytes_read = 0
    messages_read = 0

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1000000000)

    while True:
        message, client_address = sock.recvfrom(65536)
        if not message:
            break
        bytes_read += len(message)
        messages_read += 1

    print(f"Used protocol : {args.connection.upper()}")
    print(f"Number of messages read : {messages_read}")
    print(f"Number of bytes read : {bytes_read}")

    sock.close()


def udp_stop_and_wait():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (localhost, port)
    sock.bind(server_address)

    print(f"UDP-stop-and-wait listening on {localhost} : {port}")

    bytes_read = 0
    messages_read = 0

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1000000000)

    while True:
        message, client_address = sock.recvfrom(65536)
        if not message:
            break

        bytes_read += len(message)
        messages_read += 1

        response = b'ACK'
        sock.sendto(response, client_address)

    print(f"Used protocol : {args.connection.upper()}")
    print(f"Number of messages read : {messages_read}")
    print(f"Number of bytes read : {bytes_read}")

    sock.close()


parser = argparse.ArgumentParser(description='TCP/UDP Server')
parser.add_argument('-c', '--connection', type=str,
                    choices=['TCP', 'UDP'], required=True, help='connection type: TCP or UDP')
parser.add_argument('-t', '--transfer_mode', type=str, choices=[
    'streaming', 'stop-and-wait'], required=True, help='transfer mechanism: streaming or stop-and-wait')

args = parser.parse_args()

if args.connection.upper() == "TCP":
    if args.transfer_mode.lower() == "streaming":
        tcp_streaming()
    elif args.transfer_mode.lower() == "stop-and-wait":
        tcp_stop_and_wait()
    else:
        print("Transfer mechanism not supported")
        exit(0)
elif args.connection.upper() == "UDP":
    if args.transfer_mode.lower() == "streaming":
        udp_streaming()
    elif args.transfer_mode.lower() == "stop-and-wait":
        udp_stop_and_wait()
    else:
        print("Transfer mechanism not supported")
        exit(0)
else:
    print("Protocol not supported")
    exit(0)
