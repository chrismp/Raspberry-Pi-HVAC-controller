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

	if coolTemperature==None or coolTemperature=='':
		coolSwitch = 0
		coolTemperature = None
	else:
		if inTemperatureRange(minTemp, maxTemp, coolTemperature)==False:
			print('Cool temperature out of range')
			coolSwitch = 0
		else:
			if coolSwitch==1 and heatSwitch==1:
				coolSwitch = 1
				heatSwitch = 0

			if roomTemperature > int(coolTemperature):
				print('Room temperature too high. Cooling...')
			else:
				print('Room temp cool, turning off cool.')

	if heatTemperature==None or heatTemperature=='':
		heatSwitch = 0
		heatTemperature = None
	else:
		if inTemperatureRange(minTemp, maxTemp, heatTemperature)==False:
			print('Heat temp out of range')
			heatSwitch = 0
		else:
			if coolSwitch==1 and heatSwitch==1:
				coolSwitch = 0
				heatSwitch = 1

			if roomTemperature < int(heatTemperature):
				print('Room temp too cold. Heating...')
			else:
				print('Room temp warm. Turning off heat.')

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

def inTemperatureRange(minTemp, maxTemp, temperature):
	if temperature==None or temperature=='':
		return False

	if int(temperature)<minTemp or int(temperature)>maxTemp:
		return False

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