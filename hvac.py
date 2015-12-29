import requests
import random
import sys
import datetime
import time
import json
import os
import RPi.GPIO as GPIO
import dotenv


def currentTemperatureRaw():
	return random.uniform(60.0, 90.0)

def currentTemperatureRound(temperatureRaw):
	return int(round(temperatureRaw))

def currentHumidityRaw():
	return random.uniform(60.0, 90.0)

def currentHumidityRound(humidityRaw):
	return int(round(humidityRaw))

def sendCurrentStatus():
	dataToSend = {
		'roomTemperature': currentTemperatureRaw(),
		'humidity': currentHumidityRaw(),
		'coolSwitch': currentStatus['coolSwitch'],
		'coolTemperature': currentStatus['coolTemperature'],
		'heatSwitch': currentStatus['heatSwitch'],
		'heatTemperature': currentStatus['heatTemperature'],
		'fanSwitch': currentStatus['fanSwitch']
	}

	url = baseURL+'/add-hvac-status'
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
	print r.content
	rJSON = r.json()

	coolSwitch = rJSON['coolSwitch']
	coolTemperature = rJSON['coolTemperature']
	heatSwitch = rJSON['heatSwitch']
	heatTemperature = rJSON['heatTemperature']
	fanSwitch = rJSON['fanSwitch']

	setStatus(coolSwitch, coolTemperature, heatSwitch, heatTemperature, fanSwitch)

def setStatus(coolSwitch, coolTemperature, heatSwitch, heatTemperature, fanSwitch):
	minTemp = int( os.environ.get('MINIMUM_TEMPERATURE') )
	maxTemp = int( os.environ.get('MAXIMUM_TEMPERATURE') )

	roomTemperature = currentTemperatureRaw() # Replace with code for getting raw temperature read by digital temperature sensor

	if inTemperatureRange(minTemp, maxTemp, coolTemperature)==False:
		coolTemperature = None

	if inTemperatureRange(minTemp, maxTemp, heatTemperature)==False:
		heatTemperature = None

	if coolSwitch==1:
		if inTemperatureRange(minTemp, maxTemp, coolTemperature)==False:
			print 'Cool temperature out of range'
			coolSwitch = 0
			coolTemperature = None
		else:
			if coolSwitch==1 and heatSwitch==1:
				coolSwitch = 1
				heatSwitch = 0

			if roomTemperature > int(coolTemperature):
				print 'Room temperature too high. Cooling...'
			else:
				print 'Room temp cool, turning off cool.'
	else:
		print 'cool switched off'
		coolSwitch = 0

	if heatSwitch==1:
		if inTemperatureRange(minTemp, maxTemp, heatTemperature)==False:
			print 'Heat temp out of range'
			heatSwitch = 0
			heatTemperature = None
		else:
			if coolSwitch==1 and heatSwitch==1:
				coolSwitch = 0
				heatSwitch = 1

			if roomTemperature < int(heatTemperature):
				print 'Room temp too cold. Heating...'
			else:
				print 'Room temp warm. Turning off heat.'
	else:
		print 'heat switched off'
		heatSwitch = 0

	if fanSwitch==1:
		print 'fan switched on'
	else:
		print 'fan switched off'
		fanSwitch = 0

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
	# Setting up environmental variables
	# See https://github.com/theskumar/python-dotenv
	dotenvPath = os.path.join(
		os.path.dirname(__file__),
		'.env'
	)
	dotenv.load_dotenv(dotenvPath)

	# Get current status
	baseURL = os.environ.get('BASE_URL')
	statusURL = baseURL+'/status'
	statusURLResponse = requests.get(
		statusURL
	)

	startupStatus = statusURLResponse.json()
	startupStatusDictionary = startupStatus['Status']
	
	if startupStatusDictionary==None:
		currentStatus = {
			'coolSwitch': 0,
			'coolTemperature': None,
			'heatSwitch': 0,
			'heatTemperature': None,
			'fanSwitch': 0
		}
	else:
		currentStatus = {
			'coolSwitch': startupStatusDictionary['coolSwitch'],
			'coolTemperature': startupStatusDictionary['coolTemperature'],
			'heatSwitch': startupStatusDictionary['heatSwitch'],
			'heatTemperature': startupStatusDictionary['heatTemperature'],
			'fanSwitch': startupStatusDictionary['fanSwitch']
		}

	try:
		while True:
			preConnect = datetime.datetime.now()
			sendCurrentStatus()
			lastConnect = datetime.datetime.now()
			time.sleep(1)
	except Exception as e:
		raise
