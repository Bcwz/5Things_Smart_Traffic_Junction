Assuming RSSI_Scan and RSSI_Localizer have already been initialized.
ap_info = rssi.getAPinfo(networks=ssids, sudo=True)
rssi_values = [ap['signal'] for ap in ap_info]
position = localizer.getNodePosition(rssi_values)
print(position)

# prints a 1-D array holding [x,y]