import socket

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('10.0.0.4', 8090))
clientsocket.send('hello'.encode())