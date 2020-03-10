import socket, os, random, sys
from threading import Thread

port = 8888

def out_ready():
    input('Press enter to ready up')
    print('You are ready!')
    c.send(' '.encode())

def in_ready():
    c.recv(8)
    print('Opponent is ready!')

out_ready_t = Thread(target = out_ready)
in_ready_t = Thread(target = in_ready)

def ready():
    out_ready_t.start()
    in_ready_t.start()
    out_ready_t.join()
    in_ready_t.join()

print('Welcome to open-spit!')
while True:
    join_or_host = input('Would you like to join or host a game?\n>')

    if join_or_host == 'join':
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            host = input('Enter the host\'s IP address:\n>')
            try:
                c.connect((host, port))
                break
            except:
                print('Connection error')
        print('Connected to ' + host)
        ready()

    elif join_or_host == 'host':
        host = socket.gethostname()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(1)
        print('Server running from ' + host + ' on port ' + str(port))

        while True:
            print('Waiting on a client...')
            c, c_ip = s.accept()
            print(str(c_ip[0]) + ' connected from port ' + str(c_ip[1]))
            #Thread and join the ready funcs
            ready()
    elif join_or_host == 'quit':
        sys.exit()
