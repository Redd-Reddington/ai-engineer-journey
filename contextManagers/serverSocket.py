#import socket


#server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server.bind(("localhost", 9999))
#server.listen()

# work

#server.close()





#import socket


#class ServerSocket:

#    def __init__(self, host, port):
#        self.host = host
#        self.port = port


#    def __enter__(self):
#        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        self.server.bind((self.host, self.port))
#        self.server.listen()
#        return self.server


#    def __exit__(self, exc_type, exc_val, exc_tb):
#        self.server.close()


#with ServerSocket("localhost", 9999) as server:
#    server.accept()




import socket
from contextlib import contextmanager

@contextmanager
def server_socket(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host, port))
        s.listen()
        yield s
    finally:
        s.close()


with server_socket("localhost", 9999) as server:
    client, addr = server.accept()