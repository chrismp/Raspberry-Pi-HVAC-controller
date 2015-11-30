from flask import Flask, render_template, flash, redirect, jsonify, request
from collections import namedtuple
# from app import app
import datetime
import time
import db

app = Flask(__name__, static_url_path='')

# currentStatus = {
# 	'unixTime'
# 	'hvac': 0,
# 	'fan': 0,
# 	'roomTemperature': None,
# 	'cool': None,
# 	'heat': None
# }

desiredStatus = {
	'hvac': 0,
	'fan': 0,
	'cool': None,
	'heat': None
}

AcStatus = namedtuple(
	'AcStatus',
	[
		'unixTime',
		'hvacStatus',
		'fanStatus',
		'roomTemperature',
		'cool',
		'heat'
	]
)

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def homepage():
	latestStatus = db.getLastStatus()


	return render_template(
		'index.html',
		timeNow = datetime.datetime.now(),
		timeLastRead = latestStatus[1],
		hvacStatus = latestStatus[2],
		fanStatus = latestStatus[3],
		roomTemperature = latestStatus[4],
		cool = latestStatus[5],
		heat = latestStatus[6]
	)

# Receive information from the Raspberry Pi about the air conditioner's state and add to the database. 
# Respond to the Pi with the current desired state as set by the user.
@app.route('/add-hvac-status', methods=['POST'])
def update():
	response = request.json
	hvacStatus = response['hvacStatus']
	fanStatus = response['fanStatus']
	roomTemperature = response['roomTemperature']
	cool = response['cool']
	heat = response['heat']

	# add current status received from Pi to database
	db.addStatus(
		AcStatus(
			time.time(),
			hvacStatus,
			fanStatus,
			roomTemperature,
			cool,
			heat
		)
	)

	return jsonify(desiredStatus)

@app.route('/status', methods=['GET','POST'])
def status():
	# Sets new desired state based on uer input and return current state of HVAC and fan
	if request.method == 'POST':
		desiredStatus = statify(request.json)
		desiredStatusTup = (
			desiredStatus['HVAC']['status'],
			desiredStatus['Fan']['status'],
			desiredStatus['HVAC']['cool'],
			desiredStatus['HVAC']['heat']
		)

	currentLog = db.getLastStatus()
	currentStatus = (
		currentLog[1],
		currentLog[2],
		currentLog[3],
		currentLog[4],
		currentLog[5],
		currentLog[6]
	)

	return jsonify(
		unixTime = currentStatus[0],
		hvacStatus = currentStatus[1],
		fanStatus = currentStatus[2],
		roomTemperature = currentStatus[3],
		cool = currentStatus[4],
		heat = currentStatus[5]
	)

def statify(uiStatus):
	allowedStatesHVAC = {
		'OFF': {
			'status': 0,
			'cool': '',
			'heat': ''
		},
		'COOL': {
			'status': 1,
			'cool': str(uiStatus['cool']),
			'heat': ''
		},
		'HEAT': {
			'status': 2,
			'cool': '',
			'heat': str(uiStatus['heat'])
		}
	}

	allowedStatesFan = {
		'OFF': {
			'status': 0
		},
		'ON': {
			'status': 1
		}
	}

	cleanedStateHVAC = {}
	cleanedStateFan = {}

	if uiStatus['hvacMode'] == 0:
		cleanedStateHVAC = allowedStatesHVAC['OFF']
	elif uiStatus['hvacMode'] == 1:
		cleanedStateHVAC = allowedStatesHVAC['COOL']
	elif uiStatus['hvacMode'] == 2:
		cleanedStateHVAC = allowedStatesHVAC['HEAT']
	else:
		print('Invalid `hvacMode`')
		pass

	if uiStatus['fanMode'] == 0:
		cleanedStateFan = allowedStatesFan['OFF']
	elif uiStatus['fanMode'] == 1:
		cleanedStateFan = allowedStatesFan['ON']
	else:
		print('Invalid `fanMode`')
		pass


	cleanedState = {
		'HVAC': cleanedStateHVAC,
		'Fan': cleanedStateFan
	}

	return cleanedState


if __name__=='__main__':
	app.run(debug=True)