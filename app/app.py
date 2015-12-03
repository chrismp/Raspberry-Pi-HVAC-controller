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
	currentLog = db.getLastStatus()

	# Sets new desired state based on user input.
	# Return current state of HVAC and fan
	if request.method == 'POST':
		response = request.json

		# `response` won't have all the keys `desiredStatus` has.
		# So go thru each key in `desiredStatus`.
		# If a `desiredStatus` key matches a `response` key...
		# ... change that `desiredStatus` key's value... 
		# ...to that of the `response` key's value.
		# If not, still add the key to `desiredStatus`...
		# ...but give it the value from the latest reading in the data table
		for key in desiredStatus:
			if(key in response):
				desiredStatus[key] = response[key]
			else:
				desiredStatus[key] = currentLog[key]


		db.addStatus(
			AcStatus(
				time.time(),
				currentLog['roomTemperature'],
				desiredStatus['coolSwitch'],
				desiredStatus['coolTemperature'],
				desiredStatus['heatSwitch'],
				desiredStatus['heatTemperature'],
				desiredStatus['fanSwitch']
			)
		)


	print(currentLog)
	
	# do i need this...?
	# currentStatus = (
	# 	currentLog[1],
	# 	currentLog[2],
	# 	currentLog[3],
	# 	currentLog[4],
	# 	currentLog[5],
	# 	currentLog[6],
	# 	currentLog[7]
	# )

	# latestStatus = db.getLastStatus()

	return jsonify(
		timeLastRead = currentLog['unixTime'],
		roomTemperature = currentLog['roomTemperature'],
		coolSwitch = currentLog['coolSwitch'],
		coolTemperature = currentLog['coolTemperature'],
		heatSwitch = currentLog['heatSwitch'],
		heatTemperature = currentLog['heatTemperature'],
		fanSwitch = currentLog['fanSwitch']
	)


if __name__=='__main__':
	app.run(debug=True)