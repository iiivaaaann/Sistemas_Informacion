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
cur.execute("DROP TABLE RESPONSABLE")
cur.execute("CREATE TABLE if not exists RESPONSABLE (nombre text PRIMARY KEY, telefono int, rol text)")
cur.execute("CREATE TABLE if not exists DEVICES (id text primary key , ip text, responsable_nombre text, FOREIGN KEY (responsable_nombre) references responsable(nombre))")
cur.execute("CREATE TABLE if not exists ANALISIS (ID INTEGER PRIMARY KEY autoincrement, devices_id text, servicios int, servicios_ins int, detect_vulns int, FOREIGN KEY (devices_id) references DEVICES(id))")
cur.execute("DROP TABLE PUERTOS")
cur.execute("CREATE TABLE if not exists PUERTOS (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre text,analisis_id int NOT NULL, FOREIGN KEY (analisis_id) REFERENCES ANALISIS(id))")

with open("devices.json") as f:
    devices=json.load(f)
    print("Insertando responsables......")
    for i in devices:
       if i["responsable"]["telefono"]=="None":
           t=None
       else: ## Este bucle es pq si no inserta la frase NONE en lugar de meter null y para analizar es mas sencillo con Null (ademas none no es un dato valido).
           t = i["responsable"]["telefono"]
       if i["responsable"]["rol"]=="None":
           r=None
       else:
           r=i["responsable"]["rol"]

       cur.execute("INSERT OR IGNORE INTO RESPONSABLE (nombre, telefono, rol) VALUES (?,?,?)",(i["responsable"]["nombre"], t, r))
    b=cur.execute("SELECT COUNT(*) FROM RESPONSABLE").fetchall()
    print("....responsables insertados con éxito!!")
    print(str(b[0][0])+" responsables en la BBDD")
    print("Procedemos a insertar DEVICES!")
    for i in devices:
       cur.execute("INSERT OR IGNORE INTO DEVICES (id, IP, responsable_nombre) VALUES (?,?,?)",(i["id"], i["ip"],i["responsable"]["nombre"]))
    b = cur.execute("SELECT COUNT(*) FROM DEVICES").fetchall()
    print("....devices insertados con éxito!!")
    print(str(b[0][0]) + " devices en la BBDD")



conexion.commit()

