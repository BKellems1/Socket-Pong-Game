# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import json
import pygame


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 59417
        self.addr = (self.server, self.port)
        # self.id = self.connect()
        # print(self.id)
    
    def getPos(self):
        return self.pos

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(1024).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(1024).decode()
        except socket.error as e:
            print(e)


# n = Client()
# jsonData = n.client.recv(1024).decode()
# data = json.loads(jsonData)
# screenHeight = data['screenHeight']
# screenWidth = data['screenWidth']
# side = data['side']

# print('Screen Width:', screenWidth)
# print('Screen Height:', screenHeight)
# print('Player Position:', side)
# n.close()
# print(n.send("hello"))
# print(n.send("world"))




