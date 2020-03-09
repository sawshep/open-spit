import socket, os, random, tkinter, pygame, threadings

def h_s_ready():
    input('Press enter to ready up')

def h_c_ready():
    c.recv(8)
    print('Client is ready!')

print('Welcome to open-spit! ')
while True:
    join_or_host = input('Would you like to join or host a game?')
    if join_or_host == 'connect':
        host = input('Enter the host\'s IP address:')
        break

    elif connect_or_host == 'host':
        host = gethostname()
        port = 8888
        max_connections = 1
        s = socket.socket()

        s.bind((host, port))
        s.listen(max_connections)
        print('Server running...')

        while True:
            print('Waiting on a client...')

            c, c_adr = s.accept()
            print(c_adr + ' connected')

            #Thread and join the ready funcs
