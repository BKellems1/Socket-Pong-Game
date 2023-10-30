# Socket-Pong-Game

Project Description:

For this project, you will have the opportunity to design and implement the classic Atari game Pong with a twist; it will be a multiplayer game with client-server architecture.  You will create both the client and server logic using what you have learned in the socket programming lessons, allowing players to compete against each other in a game of Pong over a network connection. 

You are not expected to know how to create the actual game logic, so that has been provided for you.

Primary Task:

Client.  The client needs to communicate with the server to relay and receive information about the current game state.  The client is responsible for sending the location of the user’s Pong paddle to the server.  It will receive from the server the location of the other player’s paddle, the location of the ball and the current score.  A framework for the client code has been provided inside of pongClient.py.  You can build off of this code, or discard it entirely.

Server. The server needs to communicate with two clients simultaneously over a network using sockets.  It will need to use threads to handle the two simultaneous clients.  It is responsible for relaying the location of the other player’s paddle to the client, the location of the ball and the current score.  A framework for the server code has been provided inside of pongServer.py.  As with the client, you can build off of this code, or discard it entirely.
