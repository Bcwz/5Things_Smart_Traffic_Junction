    #!/bin/bash

import socket
import os

def Main():
    host = '172.30.138.1'
    port = 5001

    server = ('172.30.138.1'', 5000)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host,port))

    message = raw_input("-> ")
    for x in range(1,11):
            cmd = "iwconfig wlan1 station dump |grep -i signal | awk -F '{print $4}' | awk -F'=' {print $1}"
    while message != 'q':
            s.sendto(message, server)
            data, addr = s.recvfrom(1024)
            print 'Received from Alice :' + str(data)
            message = raw_input("-> ")
    for x in range(1,11):
            cmd = "iwconfig wlan1 station dump |grep -i signal | awk -F '{print $4}' | awk -F'=' {print $1}"
    s.close()

if __name__ == '__main__':
       Main()