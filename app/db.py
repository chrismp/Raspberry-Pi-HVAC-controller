import sqlite3
conn = sqlite3.connect('statuses.db', check_same_thread=False)

def makeDB():
	c = conn.cursor()
	c.execute(
		'''
			CREATE TABLE IF NOT EXISTS statuses(
				row integer primary key autoincrement,
				unixTime float,
				roomTemperature float,
				coolSwitch boolean,
				coolTemperature integer,
				heatSwitch boolean,
				heatTemperature integer,
				fanSwitch boolean
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
				roomTemperature,
				coolSwitch,
				coolTemperature,
				heatSwitch,
				heatTemperature,
				fanSwitch
			)
			VALUES (
				?,
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
	conn.row_factory = sqlite3.Row
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

# http://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query
# def dict_factory(cursor, row):
#     d = {}
#     for idx, col in enumerate(cursor.description):
#         d[col[0]] = row[idx]
#     return d

makeDB()

# try:
# 	makeDB()
# except sqlite3.OperationalError:
# 	pass