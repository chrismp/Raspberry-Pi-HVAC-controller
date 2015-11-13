import sqlite3

def getAvgTemp(tempDBFile,recordLimit):
	conn = sqlite3.connect(tempDBFile)
	c = conn.cursor()
	stmt = 'SELECT * FROM tempF ORDER BY unixTime DESC LIMIT {0}'.format(recordLimit)
	executeStmt = c.execute(stmt)
	rows = executeStmt.fetchall()
	conn.close()

	fiveTemps = [row[1] for row in rows]
	avgTemp = sum(fiveTemps)/len(fiveTemps)

	return(avgTemp)
	
