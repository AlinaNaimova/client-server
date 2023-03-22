import socket
import select

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('127.0.0.1', 12344))
server_socket.listen(5)

inputs = [server_socket]
outputs = []

while inputs:
    readable, writable, exceptional = select.select(inputs, outputs, inputs)
    
    for sock in readable:
        if sock is server_socket:
            connection, client_address = sock.accept()
            connection.setblocking(0)
            inputs.append(connection)
            outputs.append(connection)
        else:
            data = sock.recv(1024)
            if data:
                for output_sock in outputs:
                    if output_sock != sock:
                        output_sock.send(data)
            else:
                inputs.remove(sock)
                outputs.remove(sock)
                sock.close()

server_socket.close()
