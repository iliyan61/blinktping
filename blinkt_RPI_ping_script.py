#!/usr/bin/env python
import os
import time
from blinkt import set_brightness, set_pixel, show, clear
 
# clear the LEDs
set_brightness(0.1)
clear()
show()
 
# dictionary data format is - "IP", "description", status where 0 = up and 1 = down
pingdict = {
	0:["grafanahost.local","Grafana",1],
	1:["dns.local","DNS",1],
	2:["nas.local","NAS",1],
	3:["gaymer.local","Desktop",1],
	4:["65.21.89.190","ESXi Host",1],
	5:["135.181.217.230","NAS",1],
	6:["pornhub.com","pornhub",1],
	7:["google.com","google",1]
			}
 
while True:
	for x in range(8):
		# change the colour slightly whilst we are testing an IP address
		if pingdict[x][2]==0:
			set_pixel(x, 0, 0, 10)
		else:
			set_pixel(x, 0, 0, 10)
 		
 		print("")
 		print("Ping?")
		

		show()
		# ping the IP address 
		response = os.system("ping -c 1 -W 2 " + pingdict[x][0]+ " >nul")
		if response == 0:
			set_pixel(x, 0, 10, 0)
			print 'pong!', pingdict[x][1], ' is up'
			pingdict[x][2]=0
		else:
			set_pixel(x, 10, 0, 0)
			print pingdict[x][1], ' is down'
			pingdict[x][2]=1
		show()
 
	  # pause for a few seconds then loop again
	time.sleep(2)

	print("")
	print("")
	print("")