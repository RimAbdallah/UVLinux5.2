#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 11:14:35 2020

@author: ramiduye
"""

import socket
import cv2
import numpy as np
import signal
import sys

host = "172.20.11.112" #RPI3 IP adress
port = 12810 #access port to the RPI3's server 
imageNumber = 1 #index of the picture screenshut by the user 
userRequest = b"" #user request to the server 

"""
signal handler
handles the socket closing when there is a user interuption
@param signum: string = signal number 
@param frame: string = execution frame 
"""
def signal_terminate_handler(signum, frame):
    connexionToServer.close()
    print("Received signal: " + str(signum) + " closing connexion")
    sys.exit(0)
    
signal.signal(signal.SIGTERM, signal_terminate_handler) #user shutdown 
signal.signal(signal.SIGINT, signal_terminate_handler) #user interuption 


""" connexion to the RPI3's server """
connexionToServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexionToServer.connect((host, port))
print("Connexion established with the server on the port: " + str(port))




while userRequest != b"end":
    userRequest = input("Please enter your request: \n s to take a picture \n x to check the camera state\n")
    if (userRequest[0] != 's') and (userRequest[1] != 'x'):
        print("Please enter a valid command")

    else:
        """ client to server communnication  """
        userMessage = userRequest.encode() #get request
        # sending request to server 
        connexionToServer.send(userMessage)

        if(userMessage[0] == "s"):
            messageRecv = connexionToServer.recv(40960000)
            print("size of user's message = ",len(messageRecv))
            if (messageRecv):
                print("Image number: " + str(imageNumber) + "recieved")
                nparr = np.fromstring(messageRecv, np.uint8)
                imageNumpy = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                cv2.imwrite('image' + str(imageNumber) + '.jpg',imageNumpy)
                imageNumber += 1
        elif (userMessage[1] == "x"):
            messageRecv = connexionToServer.recv(1024)
            print(userMessage)


print("Connexion shutdown")
connexionToServer.close()

