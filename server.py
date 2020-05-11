'''This module holds the Server class,
which is used to establish connection between 2 clients using TCP sockets'''

# From python standard library
import threading
import pickle
import socket

# My libraries
import config
import gamedata

class Server:
    '''TCP socket server for game clients to cennect to.'''
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.bind(('', config.SERVER_PORT))
        except socket.error as error:
            print(error)
        #This is a dictionary of connected client socket objects
        self.clients = {0: None, 1: None}
        self.ready = False
        self.deck = gamedata.make_deck()
        self.listen()

    def listen(self):
        '''Listens for up to 2 connections and creates a new I/O thread for each one.'''
        self.socket.listen(2)
        print('Open to connections...')
        while True:
            client, address = self.socket.accept()
            client_id = 0 if not self.clients[0] else 1
            client.send(pickle.dumps(client_id))
            print(f'Sent ID to {address}')
            client.send(pickle.dumps(self.deck))
            print(f'Sent deck to {address}')
            self.clients[client_id] = client
            print(f'{address} connected to the server')
            threading.Thread(target=self.io_thread, args=(client, address, client_id,)).start()

    def io_thread(self, client, address, client_id):
        '''Controls the I/O of information for each client socket, and handles disconnects'''

        connected = True
        while connected:
            if self.clients[int(not client_id)]:
                try:
                    data = client.recv(2048)
                    if data:
                        self.clients[int(not client_id)].send(data)
                    else:
                        connected = False
                except socket.error as error:
                    print(error)
                    connected = False
        client.close()
        self.clients[client_id] = None
        print(f'{address} disconnected')

Server()
