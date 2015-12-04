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
		'roomTemperature': currentTemperatureRaw(),
		'coolSwitch': currentStatus['coolSwitch'],
		'coolTemperature': currentStatus['coolTemperature'],
		'heatSwitch': currentStatus['heatSwitch'],
		'heatTemperature': currentStatus['heatTemperature'],
		'fanSwitch': currentStatus['fanSwitch']
	}

	url = 'http://localhost:5000/add-hvac-status'
	headers = {
		'Content-type': 'application/json',
		'Accept': 'text/plain'
	}

	r = requests.post(
		url,
		data = json.dumps(dataToSend),
		headers = headers,
		timeout = 20
	)

	rJSON = r.json()

	coolSwitch = rJSON['coolSwitch']
	coolTemperature = rJSON['coolTemperature']
	heatSwitch = rJSON['heatSwitch']
	heatTemperature = rJSON['heatTemperature']
	fanSwitch = rJSON['fanSwitch']

	setStatus(coolSwitch, coolTemperature, heatSwitch, heatTemperature, fanSwitch)

def setStatus(coolSwitch, coolTemperature, heatSwitch, heatTemperature, fanSwitch):
	minTemp = 60
	maxTemp = 90

	roomTemperature = currentTemperatureRaw()
	# coolTemperature = int(coolTemperature)
	# heatTemperature = int(heatTemperature)

	if coolSwitch==0:
		print('cool switched off')
	elif coolSwitch==1:
		if roomTemperature > coolTemperature:
			print('room temperature too high, cooling...')
		else:
			print('room temperature cool, turning off cool...')
	else:
		pass

	if heatSwitch==0:
		print('heat switched off')
	elif heatSwitch==1:
		if roomTemperature < heatTemperature:
			print('room temperature too cold, heating...')
		else:
			print('room temperature heated, turning off heat...')
	else:
		pass

	if fanSwitch==0:
		print('fan switched off')
	elif fanSwitch==1:
		print('fan switched on')

	currentStatus['coolSwitch'] = coolSwitch
	currentStatus['coolTemperature'] = coolTemperature
	currentStatus['heatSwitch'] = heatSwitch
	currentStatus['heatTemperature'] = heatTemperature
	currentStatus['fanSwitch'] = fanSwitch

	print(currentStatus)


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
			time.sleep(1)
	except Exception as e:
		raise