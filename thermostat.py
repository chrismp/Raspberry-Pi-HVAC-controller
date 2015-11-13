# sqlite3 tut: http://www.tutorialspoint.com/sqlite/sqlite_python.htm
# https://docs.python.org/2/library/sqlite3.html

import sqlite3
import time
from random import randint


tempDBFile = 'tempF.db'
conn = sqlite3.connect(tempDBFile)

# conn.execute("DROP TABLE IF EXISTS tempF")

conn.execute(
	'''
		CREATE TABLE IF NOT EXISTS tempF(
			unixTime float,
			temp integer
		)
	'''
)


try:
	while True:
		unixTimeNow = time.time()
		temp = randint(60,90)
		c = conn.cursor()

		print("Unix time is {0}. Inserting temperature {1}F".format(unixTimeNow,temp))
		c.execute(
			'''
				INSERT INTO tempF(unixTime,temp)
				VALUES(?,?)
			''',
			(unixTimeNow,temp)
		)
		conn.commit()
		time.sleep(1)
except KeyboardInterrupt:
	conn.close()
	print('Interrupted!')