from bluepy.btle import Scanner
 
scanner = Scanner()
devices = scanner.scan(10.0)
 
for device in devices:
    print("DEV = {} RSSI = {}".format(device.addr, device.rssi))