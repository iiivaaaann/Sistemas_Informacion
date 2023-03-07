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
##cur.execute("INSERT INTO PUERTOS (nombre) VALUES ('puerto de prueba')")
#cur.execute("DROP TABLE PUERTOS")
#  FOREIGN KEY(trackartist) REFERENCES artist(artistid)
cur.execute("CREATE TABLE if not exists RESPONSABLE (nombre text PRIMARY KEY, telefono int, rol text)")
cur.execute("CREATE TABLE if not exists DEVICES (id text primary key , ip text, responsable_nombre text, FOREIGN KEY (responsable_nombre) references responsable(nombre))")
cur.execute("CREATE TABLE if not exists ANALISIS (ID INTEGER PRIMARY KEY autoincrement, devices_id text, servicios int, servicios_ins int, detect_vulns int, FOREIGN KEY (devices_id) references DEVICES(id))")
cur.execute("CREATE TABLE if not exists PUERTOS (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre text,analisis_id int, FOREIGN KEY (analisis_id) REFERENCES ANALISIS(id))")

with open("devices.json") as f:
    devices=json.load(f) # array en devices
    for i in devices:
       for j in i["analisis"]["puertos_abiertos"]:
           if j not in('N','o','n','e'):
            #cur.execute("INSERT INTO PUERTOS (nombre) VALUES (?)",(j,) )
            conexion.commit()

