'''comment from zs5656:
okay, this one is mine. it takes the input from an excel sheet and shoves it into dijixstras algorithm implementation in python, which i did NOT code.'''

from tkinter import *
from tkinter.ttk import *
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

def main():
    window = Tk()
    input_text = Label(
        text="Input start station:",
    )

    output_text = Label(
        text="Input end station:",
    )

    combo_input = Combobox(
        values=station_list
    )

    combo_output = Combobox(
        values=station_list
    )
    combo_input.place(x=50, y=50)

    def getText():
        start = db.execute("SELECT line from 'Stations' WHERE name = ?", (combo_input.get(),)).fetchone()[0] + " " + combo_input.get()
        end = db.execute("SELECT line from 'Stations' WHERE name = ?", (combo_output.get(),)).fetchone()[0] + " " + combo_output.get()
        print(f"start: {start}")
        print(f"end: {end}")
        if start == end:
            route.config(text = f"Shortest path shown, with time taken being 0 minutes and 0 seconds because they are the same station and you are a clown for trying this.\n{start[4:]} -> {start[4:]}")
            interchanges.config(text = f"Change lines from Stupidity to Unstupidity at {start[4:]}")

        else:
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
            shortened_path = [path[0]]
            for t in range(1, len(path) - 1):
                if path[t][:3] != path[t-1][:3] or path[t][:3] != path[t+1][:3]:
                    shortened_path.append(path[t])
            shortened_path.append(path[-1])
            route.config(text=f"Shortest path shown, with time taken being {travel // 60} minutes and {travel % 60} seconds.\n" + " -> ".join(shortened_path))
            interchanges.config(text="\n".join(the_interchanges))
            print(f"Shortest path shown, with time taken being {travel // 60} minutes and {travel % 60} seconds.\n" + str(" -> ".join(shortened_path)))
            print("\n".join(the_interchanges))

    button1 = Button(
        text="Click here",
        command=getText
    )

    #main_text.place(x=0, y=0)
    input_text.pack()
    combo_input.pack()
    output_text.pack()
    combo_output.pack()
    button1.pack()

    route = Label(window, text="", wraplength=300)
    route.pack()


    interchanges = Label(window, text="", wraplength=300)
    interchanges.pack()

    disclaimer = "this program doesn't account for wait times or delays. Please factor in additional time when travelling."

    disclaimer = Label(window, text =disclaimer, wraplength=300)
    disclaimer.pack()

    window.title("Python test")
    window.geometry("400x500")

    window.mainloop()

main()
db.close()