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

def isRunning():
	return True if random.randint(0, 1)==1 else False

def sendCurrentStatus():
	dataToSend = {
		# 'isRunning': isRunning(),
		'roomTemperature': currentTemperatureRound(currentTemperatureRaw()),
		'hvacStatus': desiredState['hvac'],
		'fanStatus': desiredState['fan'],
		'cool': desiredState['cool'],
		'heat': desiredState['heat']
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

	hvacStatus = r.json()['hvac']
	fanStatus = r.json()['fan']
	cool = r.json()['cool']
	heat = r.json()['heat']

	print(hvacStatus, fanStatus, cool, heat)
	setStatus(hvacStatus, fanStatus, cool, heat)

def setStatus(hvacStatus, fanStatus, cool, heat):
	roomTemperature = currentTemperatureRaw()

	if hvacStatus==1:
		hvac = 1
		coolSet = cool
		heatSet = None
	elif hvacStatus==2:
		hvac = 2
		coolSet = None
		heatSet = heat
	else:
		hvac = 0
		coolSet = None
		heatSet = None

	if fanStatus==1:
		fan = 1
	else:
		fan = 0

	currentState['hvac'] = hvac
	currentState['fan'] = fan
	currentState['cool'] = coolSet
	currentState['heat'] = heatSet


if __name__=='__main__':
	currentState = {
		'hvac': 0,
		'fan': 0,
		'cool': None,
		'heat': None
	}

	desiredState = {
		'hvac': 0,
		'fan': 0,
		'cool': None,
		'heat': None
	}

	try:
		while True:
			preConnect = datetime.datetime.now()
			sendCurrentStatus()
			lastConnect = datetime.datetime.now()
			time.sleep(5)
	except Exception as e:
		print(e)