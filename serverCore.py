import socket
import os
import struct
from _thread import *

import menuManager
import gameManager

opt_moderator = 0       # 0=Bot 1=User
opt_gamemode = 0        # 0=Normal 1=Speed
opt_timer = 0.10        # multi
opt_playRefrain = True 
opt_winScore = 10

opt_guessArtist = False
opt_guessTitle = True

opt_ignoreFeatures = True

opt_ignoreCase = True
opt_ignoreOrder = True
opt_ignoreSpecial = True
opt_ignoreAdd = True

opt_guessTime = 30      # seconds

SERVER_RUNNING = True

server_clientCount = 0
server_connections = {}

# server_status -1=error 0=offline 1=lobby 2=starting 3=ingame 4=endgame 5=restarting
server_status = 0

def start_server(port):
    # Start server in new thread
    start_new_thread(threaded_server, (port, ))

def threaded_server(port):
    global SERVER_RUNNING
    global server_status
    global server_clientCount

    ServerSocket = socket.socket()
    host = '127.0.0.1'
    server_clientCount = 0

    try:
        ServerSocket.bind((host, port))
    except socket.error as e:
        print(str(e))
        server_status = -1

    # Server got started
    # Set server status to lobby
    server_status = 1

    ServerSocket.listen(5)

    while SERVER_RUNNING:
        Client, address = ServerSocket.accept()
        start_new_thread(threaded_client, (Client, ))
        server_clientCount += 1
        
        # Update server main menu
        menuManager.update_serverMenu(['> New Client connected...'])

    ServerSocket.close()

# New client connection (new thread)
def threaded_client(connection):
    global server_clientCount
    global server_status
    global server_connections

    # Handle client message
    while True:

        try:
            size = struct.unpack("i", connection.recv(struct.calcsize("i")))[0]
            data = ""
            while len(data) < size:
                msg = connection.recv(size - len(data)).decode('utf-8')
                if not msg:
                    break
                data += msg

            handle_clientMsg(connection, data)

        except OSError as e:
            print(e)
            break
        except Exception as e:
            print(e)
            break

    connection.close()
    server_clientCount -= 1

    # Delete from connections
    remove_client(connection)

    # Update server main menu
    menuManager.update_serverMenu(['> Client disconnected...'])

    # Send clientCount to all
    send_msgToClients('[update_clientCount]' + str(server_clientCount))

    # Send connClients to all
    connClients = ''
    clientNumb = 0
    for currUsername in server_connections.keys():
        clientNumb += 1
        if(clientNumb == len(server_connections.keys())):
            connClients += currUsername
        else:
            connClients += currUsername + '[/split/]'

    send_msgToClients('[update_connClients]' + connClients)

def handle_clientMsg(connection, client_message):
    global server_connections
    
    if(client_message.startswith('[client_username]')):
        username = client_message.replace('[client_username]', '')

        # Add client to client list
        server_connections[username] = connection

        # Send info message
        send_clientMsg(connection,'[update_status]' + str(server_status))

        # Send clientCount to all
        send_msgToClients('[update_clientCount]' + str(server_clientCount))

        # Send connClients to all
        connClients = ''
        clientNumb = 0
        for currUsername in server_connections.keys():
            clientNumb += 1
            if(clientNumb == len(server_connections.keys())):
                connClients += currUsername
            else:
                connClients += currUsername + '[/split/]'

        send_msgToClients('[update_connClients]' + connClients)

    elif(client_message == '[client_guess_request]'):
        # Handle client guess request
        gameManager.handle_guess_request(connection)

    elif(client_message.startswith('[client_guess_input]')):
        # Handle client guess request
        gameManager.handle_guess_input(connection, client_message.replace('[client_guess_input]', ''))


def send_clientMsg(connection, message):
    try:
        msg = str.encode(message)

        data2 = struct.pack("i", len(msg)) + msg

        connection.send(data2)
    except OSError as e:
        print(e)

def send_msgToClients(message):
    global server_connections

    for username in server_connections.keys():
        send_clientMsg(server_connections[username], message)

def remove_client(connection):
    del server_connections[get_username(connection)]

def get_username(connection):
    global server_connections

    conn_username = ''

    # Get username from connection
    for username in server_connections.keys():

        if(server_connections[username] == connection):
            conn_username = username
            break

    if(conn_username != ''):
        return conn_username
    else:
        return None