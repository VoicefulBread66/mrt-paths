'''comment from zs5656:
okay, this one is mine. it takes the input from an excel sheet and shoves it into dijixstras algorithm implementation in python, which i did NOT code.'''

from flask import *
import dijix as a
import sqlite3

db = sqlite3.connect("MRT.db")
fetch = db.execute("SELECT station_start, station_end, between_stations FROM 'StartEnd'")
station_start = []
station_end = []
between = []
for item in fetch:
    station_start.append(item[0])
    station_end.append(item[1])
    between.append(item[2])

stations = db.execute("SELECT * from 'Stations' ORDER BY name").fetchall()
nodes = []
station_list = []
nodes.append(str(stations[0][1] + " " + stations[0][0]))
station_list.append(stations[0][0])
for item in range(1, len(stations)):
    nodes.append(str(stations[item][1] + " " + stations[item][0]))
    if stations[item-1][0] != stations[item][0]:
        station_list.append(stations[item][0])
init_graph = {}
for node in nodes:
    init_graph[node] = {}

for i in range(len(between)):
    init_graph[station_start[i]][station_end[i]] = int(between[i])

graph = a.Graph(nodes, init_graph)
db.close()

app = Flask(__name__)
@app.route("/", methods = ["GET", "POST"])
def getText():
    db = sqlite3.connect("MRT.db")
    if request.method != "POST":
        return render_template("index.html", station_list = station_list)
    start = db.execute("SELECT line from 'Stations' WHERE name = ?", (request.form["start"],)).fetchone()[0] + " " + request.form["start"]
    end = db.execute("SELECT line from 'Stations' WHERE name = ?", (request.form["end"],)).fetchone()[0] + " " + request.form["end"]
    if start == end:
        return [f"Shortest path shown, with time taken being 0 minutes and 0 seconds because they are the same station and you are a clown for trying this.\n{start[4:]} -> {start[4:]}", f"Change lines from Stupidity to Unstupidity at {start[4:]}"]
    print(f"start: {start}")
    print(f"end: {end}")
    previous_nodes, shortest_path = a.dijkstra_algorithm(graph=graph, start_node=start)
    output = a.print_result(previous_nodes, shortest_path, start_node=start, target_node=end)
    
    path = output[0]
    travel = output[1]
    the_interchanges = output[2]
    if path[0][4:] == path[1][4:]:
        travel -= int(db.execute("SELECT between_stations FROM 'StartEnd' WHERE station_start = ? AND station_end = ? OR station_start = ? AND station_end = ?", (path[0], path[1], path[1], path[0])).fetchone()[0])
        del path[0]
        del the_interchanges[0]
        
    if path[-2][4:] == path[-1][4:]:
        travel -= int(db.execute("SELECT between_stations FROM 'StartEnd' WHERE station_start = ? AND station_end = ? OR station_start = ? AND station_end = ?", (path[-2], path[-1], path[-1], path[-2])).fetchone()[0])
        del path[-1]
        del the_interchanges[-1]
        
    for t in range(len(path) - 1):
        if path[t][4:] != path[t+1][4:]:
            travel += int(db.execute("SELECT wait_time FROM 'StartEnd' WHERE station_start = ? AND station_end = ? OR station_start = ? AND station_end = ?", (path[t], path[t+1], path[t+1], path[t])).fetchone()[0])
    db.close()
    shortened_path = [path[0]]
    for t in range(1, len(path) - 1):
        if path[t][:3] != path[t-1][:3] or path[t][:3] != path[t+1][:3]:
            shortened_path.append(path[t])
    shortened_path.append(path[-1])
        
    print(f"Shortest path shown, with time taken being {travel // 60} minutes and {travel % 60} seconds.\n" + " -> ".join(shortened_path))
    print("\n".join(the_interchanges))
    return [f"Shortest path shown, with time taken being {travel // 60} minutes and {travel % 60} seconds.\n" + " -> ".join(shortened_path), "\n".join(the_interchanges)]

if __name__ == "__main__":
    app.run()