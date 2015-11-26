from flask import Flask, render_template, flash, redirect, jsonify, request
from collections import namedtuple
# from app import app
import time
import db

app = Flask(__name__, static_url_path='')

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
	print("latest status is...")
	print(latestStatus)
	return render_template(
		'index.html',
		latestStatus = latestStatus
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

	print(response)
	print(AcStatus(time.time(),hvacStatus,fanStatus,roomTemperature,cool,heat))

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

	return jsonify(desiredState)

if __name__=='__main__':
	app.run(debug=True)