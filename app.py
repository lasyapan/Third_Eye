from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import re
import os
app = Flask(__name__)
count = 0

#creation of db 
if not os.path.isfile('device.db'):
    conn = sqlite3.connect('device.db')
    curs = conn.cursor()
    curs.execute("CREATE TABLE device (id INTEGER PRIMARY KEY AUTOINCREMENT, pulse INT, temp INT, mq135 INT, mq9 INT, loc TEXT)")
    curs.execute("INSERT INTO device (id, pulse, temp, mq135, mq9, loc) VALUES (1, '77','20','300','122','28.644800,77.216721')")
    conn.commit()
    conn.close()

@app.route("/")
def main():
    conn = sqlite3.connect('device.db')
    c = conn.cursor()
    c.execute('SELECT * FROM device ORDER BY ID DESC LIMIT 1;')
    account = c.fetchone()
    c.close()
    conn.close()
    coords = re.split(r",", account[5])
    if len(coords) == 2:
        latit = coords[0] 
        longit = coords[1] 
    else: 
        latit = coords[0]
        longit = coords[0]
    
    return render_template('main.html', PULSE = account[1], TEMP = account[2], MQ135 = account[3], MQ9 = account[4], LONG = longit, LAT = latit)

@app.route("/update/APIKEY=<api_key>/PULSE=<pulse>/TEMP=<temp>/MQ135=<mq135>/MQ9=<mq9>/LOC=<loc>", methods=['GET', 'POST'])
def writetosql(api_key, pulse, temp, mq135, mq9, loc):
    if api_key == '694201a':
        conn = sqlite3.connect('device.db')
        curs = conn.cursor()
        curs.execute("INSERT INTO device VALUES(:ID, :pulse, :temp, :mq135, :mq9, :loc)", {'ID': None, 'pulse': int(pulse), 'temp': int(temp), 'mq135': int(mq135), 'mq9': int(mq9), 'loc': loc})
        conn.commit()
        curs.close()
        conn.close()
        return redirect(url_for('main'))
        
    return render_template('error.html', msg = "Make sure location coords are in this format: <latitude>,<longitude> only.")

    

if __name__ == "__main__":
    app.run()
