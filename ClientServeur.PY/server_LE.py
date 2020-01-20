#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 14:18:44 2020

@author: ramiduye
"""

import socket
import signal
import sys

"""
signal handler
handles the socket closing when there is a volontary server interuption
@param signum: string = signal number 
@param frame: string = execution frame 
"""
def signal_terminate_handler(signum, frame):
    clientConnexion.close()
    mainConnexion.close()
    print("Received signal: " + str(signum) + "\n Your server is terminated")
    sys.exit(0)
    
signal.signal(signal.SIGTERM, signal_terminate_handler)
signal.signal(signal.SIGINT, signal_terminate_handler)

host = '' #server's IP address
port = 12810 #server's access port 

""" client handler """
mainConnexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mainConnexion.bind((host, port))
mainConnexion.listen(5)
print("Server is listening on port: " + str(port))

clientConnexion, connexionInfos = mainConnexion.accept()

""" server to client communication """
messageRecv = b""
while messageRecv!= b"fin":
    messageRecv = clientConnexion.recv(1024)
    print(messageRecv.decode())
    clientConnexion.send(b"5 / 5")

print("Connexion shutdown")
clientConnexion.close()
mainConnexion.close()
