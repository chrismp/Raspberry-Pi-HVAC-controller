import requests
import random
# import signal
# import sys
import datetime
import time
# import os
# import glob
import json
# import RPi.GPIO as io

def currentTemperatureRaw():
	return random.uniform(60.0, 90.0)

def currentTemperatureRound(temperatureRaw):
	return int(round(temperatureRaw))

def sendCurrentStatus():
	dataToSend = {
		'roomTemperature': currentTemperatureRound(currentTemperatureRaw()),
		'coolSwitch': currentStatus['coolSwitch'],
		'coolTemperature': currentStatus['coolTemperature'],
		'heatSwitch': currentStatus['heatSwitch'],
		'heatTemperature': currentStatus['heatTemperature'],
		'fanSwitch': currentStatus['fanSwitch']
	}
	print(dataToSend)

	url = 'http://localhost:5000/add-hvac-status'
	headers = {
		'Content-type': 'application/json',
		'Accept': 'text/plain'
	}

	r = requests.post(
		url,
		data = json.dumps(dataToSend),
		headers = headers,
		timeout = 5
	)

	rJSON = r.json()

	coolSwitch = rJSON['coolSwitch']
	coolTemperature = rJSON['coolTemperature']
	heatSwitch = rJSON['heatSwitch']
	heatTemperature = rJSON['heatTemperature']
	fanSwitch = rJSON['fanSwitch']

	print('======')
	setStatus(dataToSend['roomTemperature'], coolSwitch, coolTemperature, heatSwitch, heatTemperature, fanSwitch)

def setStatus(roomTemperature, coolSwitch, coolTemperature, heatSwitch, heatTemperature, fanSwitch):
	# if coolSwitch==0:
	# 	# Set cool GPIO pin to HIGH
	# elif coolSwitch==1:
	# 	# Set to LOW

	# if heatSwitch==0:
	# 	# More code
	# elif heatSwitch==1:
	# 	# Even more code

	# if fanSwitch==0:
	# 	# Switch fan off or keep it off if it's already off
	# elif fanSwitch==1:
	# 	# Turn fan on or keep it on if already on

	currentStatus['roomTemperature'] = roomTemperature
	currentStatus['coolSwitch'] = coolSwitch
	currentStatus['coolTemperature'] = coolTemperature
	currentStatus['heatSwitch'] = heatSwitch
	currentStatus['heatTemperature'] = heatTemperature
	currentStatus['fanSwitch'] = fanSwitch

	# print(currentStatus)


if __name__=='__main__':
	# Initialize variables
	currentStatus = {
		'coolSwitch': 0,
		'coolTemperature': None,
		'heatSwitch': 0,
		'heatTemperature': None,
		'fanSwitch': 0
	}

	try:
		while True:
			preConnect = datetime.datetime.now()
			sendCurrentStatus()
			lastConnect = datetime.datetime.now()
			time.sleep(5)
	except Exception as e:
		raise