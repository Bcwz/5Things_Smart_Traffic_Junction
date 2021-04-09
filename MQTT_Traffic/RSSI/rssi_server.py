#!/usr/bin/python 


import socket
import os


def Main():
    host = '172.20.10.6'
    port = 5000

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    print("ALICE Started.")
    while True:
            data, addr = s.recvfrom(1024)
            print("address of bob : " + str(addr))
            print( "message from bob : " + str(data))
            data = str(data).upper()
            print("sending : " + str(data))
            
            for i in range(0,1):
            # cmd = "iw wlan1 station dump | grep -i signal | /usr/bin/awk '{print $2}' | /usr/bin/cut -d'=' -f2"
                cmd = "netsh wlan show interface"
                print(os.popen( cmd ).read())
            # dbm = int( os.popen( cmd ).read() )
            print(" recieved RSSI: " + str(addr))
            s.sendto(str.encode(data), addr)
    s.close()
if __name__  == '__main__':
        Main()