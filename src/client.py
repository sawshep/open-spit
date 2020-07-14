'''client.py
This module contains the Client class,
which sends and receives data from the socket server of the uesr's choice.
I found the idea to send and receive objects using pickle from the official pickle doccumention.'''

# From Python standard library
import socket
import pickle
import config

class Client:
    '''The client socket connection. Receives an id from the server'''
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = input('Address: ')
        self.connect()
        self.client_id = int(self.recv())
        print(f'You are client {self.client_id}')
        self.deck = self.recv()
        if self.client_id == 1:
            self.deck = self.deck[len(self.deck) // 2:] + self.deck[:len(self.deck) // 2]
        print('Received deck')

    def connect(self):
        '''Attempts to connect to the server socket. Handles timeouts.'''
        self.socket.settimeout(5)
        try:
            self.socket.connect((self.address, config.CLIENT_PORT))
        except socket.timeout:
            print('Connection timed out')
        self.socket.settimeout(None)

    def recv(self):
        '''A one-off receive method'''
        recv = pickle.loads(self.socket.recv(2048))
        return recv

    def network_io(self, send):
        '''Handles the sending and receiving of data from the server.'''
        self.socket.send(pickle.dumps(send))
        return self.recv()
    def close(self):
        '''Closes the socket'''
        # self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
