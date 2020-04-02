import socket

#parameters for server
host = socket.gethostname()
port = 9999
max_connections = 1
header_size = 6

#creates server
s = socket.socket()
s.bind((host, port))
s.listen(max_connections)
print('Server socket created')

while True:
    print(str(host) + ' is listening on port ' + str(port) + ' for up to ' + str(max_connections) + ' connection(s)')

    #accepts any incoming connections
    c, c_ip = s.accept()
    print('Connection to ' + str(c_ip) + ' established')

    while True:
        #enter command
        cmd = input('Enter command:\n>')
        # up to 999,999 chars
        cmd = (str(len(cmd)).ljust(header_size, ' ') + cmd)

        #exit parameters, drops connection
        if cmd[header_size:len(cmd)] == 'exit':
            c.send(cmd.encode())
            print('Waiting for client socket to close...')
            c.recv(8)
            print('Closing server socket...')
            print('Connection to ' + str(c_ip) + ' dropped')
            c.close()
            break

        #send the command to the client
        else:
            c.send(cmd.encode())
            print('Command sent...')
            c.recv(8)
            print('Command excecuted')
