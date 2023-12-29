# Receiver

import socket
import sys


def start_server(_host, _port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((_host, _port))
    server_socket.listen(1)
    print(f"Server listening on {_host}:{_port}")

    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    file_name_length = int.from_bytes(client_socket.recv(1), byteorder='big')
    file_name = client_socket.recv(file_name_length).decode(
        'utf-8', 'replace').rstrip('\x00')

    print(f"Receiving file: {file_name}")

    with open(file_name, 'wb') as file:
        data = client_socket.recv(1024)
        while data:
            file.write(data)
            data = client_socket.recv(1024)

    print("File received successfully.")
    client_socket.close()
    server_socket.close()

    return 0


if __name__ == "__main__":
    if (not (len(sys.argv) == 3)):
        print(f"Usage: {sys.argv[0]} server-hostname server-port \n")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    sys.exit(start_server(host, port))
