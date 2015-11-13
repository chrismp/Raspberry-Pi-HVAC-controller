import sqlite3

tempDBFile = 'tempF.db'
conn = sqlite3.connect(tempDBFile)
c = conn.cursor()
stmt = c.execute('SELECT * FROM tempF ORDER BY unixTime DESC LIMIT 5')
rows = stmt.fetchall()
conn.close()

acStatus = None
coolTrigger = 75
fiveTemps = [row[1] for row in rows]
avgTemp = sum(fiveTemps)/len(fiveTemps)

if avgTemp>coolTrigger:
	acStatus = 'ON'
else:
	acStatus = 'OFF'

print('''Thermostat set to {0}. 
Average temperature is {1}F. 
Air conditioning is {2}'''
.format(coolTrigger,avgTemp,acStatus)
)