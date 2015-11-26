import sqlite3
conn = sqlite3.connect('statuses.db', check_same_thread=False)

def makeDB():
	c = conn.cursor()
	c.execute(
		'''
			CREATE TABLE IF NOT EXISTS statuses(
				row integer primary key autoincrement,
				unixTime float,
				hvacStatus integer,
				fanStatus integer,
				roomTemperature float,
				cool integer,
				heat integer
			)
		'''
	)
	conn.commit()

def addStatus(status):
	c = conn.cursor()
	c.execute(
		'''
			INSERT INTO statuses(
				unixTime,
				hvacStatus,
				fanStatus,
				roomTemperature,
				cool,
				heat
			)
			VALUES (
				?,
				?,
				?,
				?,
				?,
				?
			)
		''',status
	)
	conn.commit()

def getLastStatus():
	c = conn.cursor()
	c.execute(
		'''
			SELECT *
			FROM statuses
			ORDER BY row DESC 
			LIMIT 1
		'''
	)
	data = c.fetchone()
	return data


makeDB()

# try:
# 	makeDB()
# except sqlite3.OperationalError:
# 	pass