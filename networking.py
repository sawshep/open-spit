import socket
from threading import Thread
import pickle
import mechanics


class Networker:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Both networkers receive data the same way
    def recv(self):
        while True:
            self.recv_msg, self.addr = self.s.recvfrom(2048)
            self.recv_keys = pickle.loads(self.recv_msg)
            print(self.recv_keys)

class Host(Networker):
    def __init__(self):
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('127.0.0.1', port))
        print(self.s.getsockname())
        self.recv_msg, self.addr = self.s.recvfrom(2048)
        self.send_thread = Thread(target=self.send)
        self.recv_thread = Thread(target=self.recv)
        self.send_thread.start()
        self.recv_thread.start()
        self.send_thread.join()
        self.recv_thread.join()

    def send(self):
        while True:
            self.send_keys = mechanics.get_keys()
            if self.send_keys:
                self.send_msg = pickle.dumps(self.send_keys)
                self.s.sendto(self.send_msg, self.addr)

class Client(Networker):
    def __init__(self, addr):
        self.addr = addr
        # Hangs until the host receive the package.
        # TODO?: Might cause an infinite wait if there is package loss, put in loop?
        #self.s.sendto(''.encode(), (self.addr))
        #print('Connection successful')

        # Thread setup
        self.send_thread = Thread(target=self.send)
        self.recv_thread = Thread(target=self.recv)
        self.send_thread.start()
        self.recv_thread.start()
        self.send_thread.join()
        self.recv_thread.join()

    # The client sends only important key presses to the host
    def send(self):
        while True:
            self.send_keys = mechanics.get_keys()
            if self.send_keys:
                self.send_msg = pickle.dumps(self.send_keys)
                self.s.sendto(self.send_msg, (self.addr, port))
