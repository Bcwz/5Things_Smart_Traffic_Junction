import rssi

interface = 'wlan0'
rssi_scanner = rssi.RSSI_Scan(interface)

ssids = ['dd-wrt','linksys']

# sudo argument automatixally gets set for 'false', if the 'true' is not set manually.
# python file will have to be run with sudo privileges.
ap_info = rssi_scanner.getAPinfo(networks="YipResidence_5G", sudo=True)

print(ap_info)

from rssi import RSSI_Localizer


accessPoint = {
     'signalAttenuation': 3, 
     'location': {
         'y': 1, 
         'x': 1
     }, 
     'reference': {
         'distance': 4, 
         'signal': -50
     }, 
     'name': 'dd-wrt'
}

rssi_localizer_instance = RSSI_Localizer(accessPoint)
signalStrength = -69

distance = rssi_localizer_instance.getDistanceFromAP(accessPoint, signalStrength)
print(distance)

rssi_values = [ap['signal'] for ap in ap_info]
print("values" = rssi_values)
position = distance.getNodePosition(rssi_values)
print(position)
