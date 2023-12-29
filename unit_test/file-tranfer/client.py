# Sender

import socket
import sys


def send_file(_host, _port, _file_path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((_host, _port))

    file_name = _file_path.split("/")[-1]
    file_name_len =(len(file_name))
    byte_representation = (file_name_len).to_bytes((file_name_len.bit_length() + 7) // 8, 'big')
    
    client_socket.send(byte_representation)
    client_socket.send(file_name.encode())

    with open(_file_path, 'rb') as file:
        data = file.read(1024)
        while data:
            client_socket.send(data)
            data = file.read(1024)

    print(f"File {file_name} sent successfully")
    client_socket.close()
    return 0


if __name__ == "__main__":
    if (not (len(sys.argv) == 4)):
        print(f"Usage: {sys.argv[0]} server-hostname server-port file-path \n")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    file_path = sys.argv[3]

    sys.exit(send_file(host, port, file_path))
