import socket, random, _tkinter
from tkinter import *
from threading import Thread
from sys import exit
from requests import get

def ready():
    out_ready_t.start()
    in_ready_t.start()
    out_ready_t.join()
    in_ready_t.join()

def join_server():
    title_screen_frame.pack_forget()
    title_screen_frame.destroy()
    join_screen_frame.pack()
    host_ip_label.pack()
    host_ip_entry.pack()
    host = host_ip_entry.get()
    enter_host_ip_button.pack()
    back_button.pack()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def connect():
    host = host_ip_entry.get()
    try:
        c.connect((host, port))
    except:
        connection_error_label.pack()

def host_server():
    title_screen_frame.pack_forget()
    title_screen_frame.destroy()
    connection_frame.pack()
    server_address_label.pack()
    host_screen_frame.pack()
    waiting_lable.pack()
    back_button.pack()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', port))

'''
    colors = ['R ', 'G ', 'B ', 'P ']
    deck = []
    for n in range(1, 14):
        for c in colors:
            deck.append(c + str(n))
    random.shuffle(deck)
'''

def back():
    main_frame.destroy()

while True:
    port = 8888
    host = get('https://ipapi.co/ip').text

    root = Tk()
    root.geometry('500x150')
    root.title('Open-Spit')
    main_frame = Frame(root)

    back_button = Button(main_frame, text='Back', command = back)

    title_screen_frame = Frame(main_frame)
    #---------------------------------
    welcome_label = Label(title_screen_frame, text='Welcome to Open-Spit!')
    join_game_button = Button(title_screen_frame, text='Join Game', command=join_server)
    host_game_button = Button(title_screen_frame, text='Host Game', command=host_server)

    join_screen_frame = Frame(main_frame)
    #-------------------------
    host_ip_label = Label(join_screen_frame, text='Enter the host\'s IPv4 address')
    host_ip_entry = Entry(join_screen_frame, text='test')
    enter_host_ip_button = Button(join_screen_frame, text='Connect', command=connect)
    connection_error_label = Label(join_screen_frame, text='Connection error, try again')

    host_screen_frame = Frame(main_frame)
    #--------------------------
    waiting_lable = Label(host_screen_frame, text='Waiting on client...')

    connection_frame = Frame(main_frame)
    #----------------------------
    server_address_label = Label(connection_frame, text='Server running at {} on port {}'.format(host, str(port)))


    game_frame = Frame(main_frame)
    #------------------

    main_frame.pack()
    title_screen_frame.pack()
    welcome_label.pack()
    join_game_button.pack()
    host_game_button.pack()
    input('')
