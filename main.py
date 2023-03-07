import pandas as pd
import sqlite3
import json
conexion= sqlite3.connect('pr1_SI.db')
cur=conexion.cursor()
#cur.execute("DROP TABLE ALERTS")
#cur.execute("CREATE TABLE ALERTS (id INTEGER PRIMARY KEY AUTOINCREMENT, time date, sid int , msg text, clasification text, priority int, protocolo text, origen text, destino text, puerto int)")
#cur.execute("INSERT INTO ALERTS VALUES('10/10/2022', 1, 'ASD', 'IOP', 1, 'TCPPCPCP','123.123.123','234.23.24',787)")
#cur.execute("DELETE FROM ALERTS WHERE SID='1'")
#conexion.commit()
#cur.execute("CREATE TABLE IF NOT EXISTS DEVICES (id text PRIMARY KEY, ip text, localizacion text, responsable text)")
#cur.execute("CREATE TABLE PUERTOS (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre text)")
with open("devices.json") as f:
    devices=json.load(f) # array en devices
    for i in devices:
       for j in i["analisis"]["puertos_abiertos"]:
           if j not in('N','o','n','e'):
            print(j)
            cur.execute("INSERT INTO PUERTOS (nombre) VALUES(?)", j)