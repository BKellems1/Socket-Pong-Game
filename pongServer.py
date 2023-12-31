# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import threading
import json

# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games


# clients need to be updated based on: score, ball position and enemy position

server_address = ("localhost",59417)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # Creating the server
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # Working on localhost need this


try: # try to connect if fail then record why
    server.bind(server_address)
except socket.error as e:
    str(e)



server.listen(2) # needed to have listening, blank = possibility for unlimited connections
print("Waiting for connect, Server Started")

def sendInitData(conn, side):
    initial = {
        'screenHeight' : 480,
        'screenWidth' : 480,
        'side': side
    }

    # Convert the dictionary to a JSON string
    json_data = json.dumps(initial)

    # Send the JSON data to the client
    conn.sendall(json_data.encode())



def threaded_client(conn, side):
    conn.send(str.encode("Connected!"))
    sendInitData(conn,side)

    reply = ""
    while True: # server loop
        # when a client connects, assign the first one to connect as player 1, send them back the game settings, send back a json dictionary 
        # this dict will have (screen width, height & player paddle, "left or "right) in it. 
        # for testing purposes brandon, have the the client print out all the values
        try:
            data = conn.recv(1024) # larger size = more time to recv info
            reply = data.decode("utf-8")

            if not data:
                print("disconnect")
                break
            else:
                print("Received: ", reply)
                print("sending: ", reply)

            conn.sendall(str.encode(reply))
        except:
            break


    print("Lost Connection")
    conn.close()





while True: # coninuosly look for connections
    # clientConn, clientAddress = server.accept()
    # print("Connected to: ", clientAddress)
    # # start_new_thread(threaded_client,(clientConn,))
    # client_thread = threading.Thread(target=threaded_client, args=(clientConn,))
    # client_thread.start()


    # maybe change these later so that more players can join
    # Accept the first player as the left player
    left_player_conn, left_player_address = server.accept()
    print("Left Player Connected to: ", left_player_address)
    left_player_thread = threading.Thread(target=threaded_client, args=(left_player_conn, 'left'))
    left_player_thread.start()

    # Accept the second player as the right player
    right_player_conn, right_player_address = server.accept()
    print("Right Player Connected to: ", right_player_address)
    right_player_thread = threading.Thread(target=threaded_client, args=(right_player_conn, 'right'))
    right_player_thread.start()


# def start_new_game(conn):
#     # Start a new game thread for each client
#     player_position = 'Left' if len(games) % 2 == 0 else 'Right'
#     game_thread = threading.Thread(target=threaded_client, args=(conn, player_position))
#     games.append(game_thread)
#     game_thread.start()


# while True:
#     client_conn, client_address = server.accept()
#     print("Player Connected to: ", client_address)

#     # Start a new game for the connected client
#     start_new_game(client_conn)


# message = clientConn.recv(1024)               # Expect "Hello Server"

# print(f"Client sent: {message.decode()}")

# clientConn.send("Hello client.".encode())

# msg = ""
# while msg != "quit":
#     msg = clientConn.recv(1024).decode()          # Received message from client
#     print(f"Client sent: {msg}")
#     clientConn.send(msg.encode())



# clientConn.close()
# server.close()
