import sqlite3

tempDBFile = 'tempF.db'
conn = sqlite3.connect(tempDBFile)
c = conn.cursor()
stmt = c.execute('SELECT * FROM tempF ORDER BY unixTime DESC LIMIT 5')
rows = stmt.fetchall()
conn.close()

fiveTemps = [row[1] for row in rows]
avgTemp = sum(fiveTemps)/len(fiveTemps)
