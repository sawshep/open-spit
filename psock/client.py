import socket

host = socket.gethostname()
port = 9999
header_size = 6

s = socket.socket()
print('Client socket created')

s.connect((host, port))

print('Connection to ' + str(host) + ' on port ' + str(port) + ' established')

while True:
    ini_cmd = ''
    incoming = True
    #Assembles the packages into a string
    print('Waiting for command...')
    while True:
        pkt = s.recv(10)

        #detects header
        if incoming:
            print('Incoming command:')
            cmd_len = int(pkt[0:header_size - 1].decode())
            incoming = False

        #builds the initial command
        ini_cmd += pkt.decode()

        #detects if command is finished building
        if len(ini_cmd) - header_size == cmd_len:
            #strips header from command
            cmd = ini_cmd[header_size:len(ini_cmd)]
            print(cmd)
            if cmd == 'exit':
                print('Closing client socket...')
                s.send(' '.encode())
                break

            s.send(' '.encode())
            print('Command excecuted')
            break
    if cmd == 'exit':
        break
print('Connection to ' + host + ' dropped')
s.close()
