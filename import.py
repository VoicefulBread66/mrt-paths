import sqlite3
db = sqlite3.connect("MRT.db")
db.execute("DROP TABLE IF EXISTS 'StartEnd'")
db.execute("DROP TABLE IF EXISTS 'Stations'")
db.execute("CREATE TABLE 'Stations' ('name'	TEXT NOT NULL, 'line' TEXT NOT NULL)")
db.execute("CREATE TABLE 'StartEnd' ('station_start' TEXT NOT NULL, 'station_end' TEXT NOT NULL, 'between_stations' INTEGER NOT NULL, 'wait_time' INTEGER NOT NULL)")

file = open("StartEnd.csv")
for line in file.readlines()[1:]:
  db.execute("INSERT INTO 'StartEnd' VALUES (?, ?, ?, ?)", tuple(line.strip().split(",")))
file.close()

file = open("Stations.csv")
for line in file.readlines()[1:]:
  line = line.strip()
  db.execute("INSERT INTO 'Stations' VALUES (?, ?)", (line[4:], line[:3]))
file.close()

db.commit()
db.close()