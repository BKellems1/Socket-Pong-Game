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
Lock = threading.Lock()

PACKAGESIZE = 1024 # i dont know if this is a good approach but it prevents maaaggiiiccc numberrss
server_address = ("localhost",59417)

connections = []
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
    if conn not in connections:
       connections.append(conn)
    sendInitData(conn,side)

    while True: # server loop
        # when a client connects, assign the first one to connect as player 1, send them back the game settings, send back a json dictionary 
        # this dict will have (screen width, height & player paddle, "left or "right) in it. 
        # for testing purposes brandon, have the the client print out all the values
        try:
            # the data recv should be the JSON with values
            # i am confused by this part, should the update json be 
            # different than the sync json? of should we treat both dicts the same
            # also if the json is nonsync then does it really matter if the server
            # understands the data? or can we just forward it to the other client?
            jsonData = conn.recv(PACKAGESIZE)
            print("received ", jsonData, "\n")
            reply = json.loads(jsonData.decode())

            # side = data['side']
            # paddlePos = data['paddlePos']
            # ballPos = data['ballPos']
            # scores = data['scores']

            if not reply:
                print("disconnect")
                break
            
            if reply['side'] == "left":
                # in my head if the reply side is left you have to send left's data to
                # the person on the right and vice-versa. Clearly this is not working, though.
                print("sending ", reply, "to", connections[1], "\n")
                reply = json.dumps(reply)
                connections[0].sendall(reply.encode())
            elif reply['side'] == "right":
                print("sending ", reply, "to", connections[0], "\n")
                reply = json.dumps(reply)
                connections[1].sendall(reply.encode())
            

        except:
            break


    print("Lost Connection")
    conn.close()





while True: # continuously look for connections
    numConnects = []
    # Accept the first player as the left player
    while(len(numConnects) < 2):
        left_player_conn, left_player_address = server.accept()
        print("Left Player Connected to: ", left_player_address)
        left_player_thread = threading.Thread(target=threaded_client, args=(left_player_conn, 'left'))
        numConnects.append(left_player_thread)

    # Accept the second player as the right player
        right_player_conn, right_player_address = server.accept()
        print("Right Player Connected to: ", right_player_address)
        right_player_thread = threading.Thread(target=threaded_client, args=(right_player_conn, 'right'))
        numConnects.append(right_player_thread)

    left_player_thread.start()
    right_player_thread.start()
    # i am not sure if we can access thread1 and thread2 json data down here?






# while True:
#     client_conn, client_address = server.accept()
#     print("Player Connected to: ", client_address)

#     # Start a new game for the connected client
#     start_new_game(client_conn)

# Maintain a list of connected client pairs and a lock to synchronize access to it
# client_pairs = []
# client_pairs_lock = threading.Lock()

# def broadcast_data(sender_index, data):
#     global client_pairs

#     # Find the pair for the sender and send data only to that pair
#     with client_pairs_lock:
#         sender_pair = None
#         for pair in client_pairs:
#             if sender_index in pair:
#                 sender_pair = pair
#                 break

#         if sender_pair:
#             for i in sender_pair:
#                 if i != sender_index:
#                     try:
#                         sender_pair[i].sendall(json.dumps(data).encode())
#                     except Exception as e:
#                         print(f"Error sending data to client {i}: {e}")

# # Modify your threaded_client function to store the client's index and pair
# def threaded_client(conn, index, pair):
#     # existing code

#     while True:
#         try:
#             jsonData = conn.recv(PACKAGESIZE)
#             data = json.loads(jsonData.decode())

#             if not data:
#                 print("disconnect")
#                 break
#             else:
#                 print("Received: ", data)

#             # Broadcast the received data to the corresponding partner
#             broadcast_data(index, data)

#             conn.sendall(str.encode(reply))
#         except:
#             break

# # Modify your main server loop to pair up clients
# while True:
#     client_conn, client_address = server.accept()
#     print("Player Connected to: ", client_address)

#     # Add the new client to the list and pair it with the previous client
#     with client_pairs_lock:
#         if not client_pairs or len(client_pairs[-1]) == 2:
#             client_pairs.append([client_conn])
#         else:
#             client_pairs[-1].append(client_conn)

#         pair = client_pairs[-1]
#         index = len(pair) - 1

#         client_thread = threading.Thread(target=threaded_client, args=(client_conn, index, pair))
#         client_thread.start()







# clientConn.close()
# server.close()