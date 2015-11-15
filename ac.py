import sqlite3
import time

try:
	while True:

		acMasterSwitchOn = True # External variable

		if acMasterSwitchOn:
			coolTemperatureSetting = 75 # External variable
			print('AC set at {0}F'.format(coolTemperatureSetting))

			tempDBFile = 'tempF.db'
			conn = sqlite3.connect(tempDBFile)
			c = conn.cursor()
			stmt = c.execute('SELECT * FROM tempF ORDER BY unixTime DESC LIMIT 1')
			tempData = stmt.fetchone() # (1447620892.6297102, 66)
			unixTime = tempData[0]
			tempF = tempData[1]

			print('Temperature is {0}F as of {1}'.format(tempF,unixTime))
			if tempF>coolTemperatureSetting:
				# Code to set A/C GPIO to LOW
				print('Turning AC on')
			else:
				# Code to set A/C GPIO to HIGH
				print('Turning AC off')

			print('===')

			secondsBetweenReadings = 10 # external variable
			time.sleep(secondsBetweenReadings)
		else:
			# Code to set A/C GPIO to HIGH
			print('A/C switch is off. No action taken.')
except KeyboardInterrupt:
	conn.close()
	print('Interrupted!')