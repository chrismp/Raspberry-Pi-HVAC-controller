from flask import Flask, render_template, flash, redirect, jsonify, request
from collections import namedtuple
# from app import app
import datetime
import time
import db

app = Flask(__name__, static_url_path='')


desiredStatus = {
	'coolSwitch': 0,
	'coolTemperature': None,
	'heatSwitch': 0,
	'heatTemperature': None,
	'fanSwitch': 0
}

AcStatus = namedtuple(
	'AcStatus',
	[
		'unixTime',
		'roomTemperature',
		'coolSwitch',
		'coolTemperature',
		'heatSwitch',
		'heatTemperature',
		'fanSwitch'
	]
)

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def homepage():
	return render_template('index.html')

# Receive information from the Raspberry Pi about the air conditioner's state and add to the database. 
# Respond to the Pi with the current desired state as set by the user.
@app.route('/add-hvac-status', methods=['POST'])
def update():
	response = request.json
	roomTemperature = response['roomTemperature']
	coolSwitch = response['coolSwitch']
	coolTemperature = response['coolTemperature']
	heatSwitch = response['heatSwitch']
	heatTemperature = response['heatTemperature']
	fanSwitch = response['fanSwitch']

	# add current status received from Pi to database
	db.addStatus(
		AcStatus(
			time.time(),
			roomTemperature,
			coolSwitch,
			coolTemperature,
			heatSwitch,
			heatTemperature,
			fanSwitch
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
		currentLog[6],
		currentLog[7]
	)

	latestStatus = db.getLastStatus()

	return jsonify(
		timeLastRead = latestStatus[1],
		roomTemperature = latestStatus[2],
		coolSwitch = latestStatus[3],
		coolTemperature = latestStatus[4],
		heatSwitch = latestStatus[5],
		heatTemperature = latestStatus[6],
		fanSwitch = latestStatus[7]
	)

# def statify(uiStatus):
# 	allowedStatesHVAC = {
# 		'OFF': {
# 			'status': 0
# 		},
# 		'COOL': {
# 			'status': 1,
# 			'temperature': uiStatus['cool']
# 		},
# 		'HEAT': {
# 			'status': 2,
# 			'temperature': uiStatus['heat']
# 		}
# 	}

# 	allowedStatesFan = {
# 		'OFF': {
# 			'status': 0
# 		},
# 		'ON': {
# 			'status': 1
# 		}
# 	}

# 	cleanedStateHVAC = {}
# 	cleanedStateFan = {}

# 	if uiStatus['hvacMode'] == 0:
# 		cleanedStateHVAC = allowedStatesHVAC['OFF']
# 	elif uiStatus['hvacMode'] == 1:
# 		cleanedStateHVAC = allowedStatesHVAC['COOL']
# 	elif uiStatus['hvacMode'] == 2:
# 		cleanedStateHVAC = allowedStatesHVAC['HEAT']
# 	else:
# 		print('Invalid `hvacMode`')
# 		pass

# 	if uiStatus['fanMode'] == 0:
# 		cleanedStateFan = allowedStatesFan['OFF']
# 	elif uiStatus['fanMode'] == 1:
# 		cleanedStateFan = allowedStatesFan['ON']
# 	else:
# 		print('Invalid `fanMode`')
# 		pass


# 	cleanedState = {
# 		'HVAC': cleanedStateHVAC,
# 		'Fan': cleanedStateFan
# 	}

# 	return cleanedState


if __name__=='__main__':
	app.run(debug=True)