import pandas as pd
import sqlite3
conexion= sqlite3.connect('pr1_SI.db')
cur=conexion.cursor()
#cur.execute("CREATE TABLE ALERTS (time date, sid int, msg text, clasification text, priority int, protocolo text, origen text, destino text, puerto int)")
#cur.execute("INSERT INTO ALERTS VALUES('10/10/2022', 1, 'ASD', 'IOP', 1, 'TCPPCPCP','123.123.123','234.23.24',787)")
#cur.execute("DELETE FROM ALERTS WHERE SID='1'")
#conexion.commit()
