# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import threading

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



def threaded_client(conn):
    
    reply = ""
    while True:
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





while True: # coninuosly look for connections
    clientConn, clientAddress = server.accept()
    print("Connected to: ", clientAddress)
    # start_new_thread(threaded_client,(clientConn,))
    client_thread = threading.Thread(target=threaded_client, args=(clientConn,))
    client_thread.start()





# message = clientConn.recv(1024)               # Expect "Hello Server"

# print(f"Client sent: {message.decode()}")

# clientConn.send("Hello client.".encode())

msg = ""
while msg != "quit":
    msg = clientConn.recv(1024).decode()          # Received message from client
    print(f"Client sent: {msg}")
    clientConn.send(msg.encode())



clientConn.close()
server.close()
