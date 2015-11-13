from functions import getAvgTemp

acStatus = None
acOn = True # External variable


if acOn==True:
	avgTemp = getAvgTemp('tempF.db',5)
	coolTrigger = 75 # External variable
	print('Average temperature is {0}F. Thermostat set to {1}F'.format(avgTemp,coolTrigger))
	if avgTemp>coolTrigger:
		acStatus = 'ON'
		print('Air conditioner turned on')
	else:
		acStatus = 'OFF'
		print('Air conditioner turned off')
else:
	acStatus = 'OFF'
	print('Air conditioner switched off')

