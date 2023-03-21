import pandas as pd
import sqlite3
import json
import matplotlib.pyplot as plt
conexion= sqlite3.connect('pr1_SI.db')
cur=conexion.cursor()

cur.execute("CREATE TABLE if not exists RESPONSABLE (nombre text PRIMARY KEY, telefono int, rol text)")
cur.execute("CREATE TABLE if not exists DEVICES (id text primary key , ip text, responsable_nombre text, FOREIGN KEY (responsable_nombre) references responsable(nombre))")
cur.execute("CREATE TABLE if not exists ANALISIS (ID INTEGER PRIMARY KEY autoincrement, devices_id text UNIQUE, servicios int, servicios_ins int, detect_vulns int, FOREIGN KEY (devices_id) references DEVICES(id))")
cur.execute("CREATE TABLE if not exists PUERTOS (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre text,analisis_id int NOT NULL, FOREIGN KEY (analisis_id) REFERENCES ANALISIS(id) CONSTRAINT NOT_REPEATED_PORTS_ANALISIS UNIQUE (nombre, analisis_id))")

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
    print("Procediendo a insertar ANÁLISIS.....")
    for i in devices:
        cur.execute("INSERT OR IGNORE INTO ANALISIS (DEVICES_ID, SERVICIOS, SERVICIOS_INS,DETECT_VULNS) VALUES (?,?,?,?)", (i["id"],i["analisis"]["servicios"],i["analisis"]["servicios_inseguros"], i["analisis"]["vulnerabilidades_detectadas"]))
    print("..... análisis insertados")
    b = cur.execute("SELECT COUNT(*) FROM DEVICES").fetchall()
    print(str(b[0][0])+" analisis en la BBDD")
#Para insertar en la tabla puertos debemos ver qué puertos abiertos hay en X dispositivo y buscar su analisis_id en la BD
    for i in devices:
        #print("Device id: " + i["id"])
        #print("Analisis id: " + str(cur.execute("SELECT ID FROM ANALISIS WHERE DEVICES_ID=?", (i["id"],)).fetchall()[0][0]))
        #print("Puertos abiertos: " + str(i["analisis"]["puertos_abiertos"]))
        analisis_id=cur.execute("SELECT ID FROM ANALISIS WHERE DEVICES_ID=?", (i["id"],)).fetchall()[0][0]
        for j in i["analisis"]["puertos_abiertos"]:
            if i["analisis"]["puertos_abiertos"]!="None":
                name=j
                #print("nombre: " + name + " id analisis: " + str(analisis_id))
                cur.execute("INSERT OR IGNORE INTO PUERTOS (NOMBRE, ANALISIS_ID) VALUES (?,?)",(name,analisis_id))
    print(".... puertos insertados correctamente!")


conexion.commit()


#Ejer 2

#1. Número de dispositivos
#Basando en IPs diferentes
df=pd.read_sql_query("SELECT DISTINCT origen FROM ALERTS UNION SELECT DISTINCT destino FROM ALERTS ",conexion)
print("Número de dispotivos = " + str(df.size) + " dispostivos")

#2. Número de alertas

df=pd.read_sql_query("SELECT sid FROM ALERTS ",conexion)
print("Número de alertas = " + str(df.size) + " alertas")

#3. Media y desviación estándar del totla de puertos abiertos
df=pd.read_sql_query("SELECT puerto FROM ALERTS ",conexion)

print("Media = " + str(df.mean()) )
print("Desviación estándar = " + str(df.std()))

#4. Media y desviación est´andar del número de servicios inseguros detectados

#5. Media y desviación estándar del número de vulnerabilidades detectadas.

#6. Valor mínimo y valor máximo del total de puertos abiertos.


#7. Valor mínimo y valor máximo del número de vulnerabilidades detectadas.




#Ejer 4

#1. Mostrar las 10 IP de origen más problemáticas, representadas en un gráfico de barras (las IPs de origen más problemáticas son las que más alertas han generado con prioridad 1).
#df=pd.read_sql_query("SELECT COUNT(*) as num, origen FROM ALERTS WHERE priority = 1 GROUP BY origen ORDER BY num desc",conexion)
df=pd.read_sql_query("SELECT COUNT(*) as num, origen FROM ALERTS WHERE priority = 1 GROUP BY origen ORDER BY num desc",conexion)
muestra=df[:10].copy()
x_values=muestra['origen']
y_values=muestra['num']
"""print(df['origen'])
x_values=df['origen'].unique().
y_values=df['origen'].value_counts().tolist()"""
plt.figure(num=None, figsize=(14, 6), dpi=80, facecolor='w', edgecolor='k')
plt.bar(x_values,y_values)
plt.show()
plt.close("all")
#2. Número de alertas en el tiempo, representadas en una serie temporal.
df=pd.read_sql_query("SELECT time FROM ALERTS ",conexion)
df.index=df['time']
print(df)
#3. Número de alertas por categoríaa, representadas en un gráfico de barras.
df=pd.read_sql_query("SELECT COUNT(*) as num, clasification FROM ALERTS GROUP BY clasification ORDER BY num desc ",conexion)
print(df)
plt.figure(num=None, figsize=(18, 10), dpi=80, facecolor='w', edgecolor='k')
x_values=['GPCD','MA','PBT','NST','PCPV','AIL','AAPG','DNS','WAA','NT','APVWA','AUPG','IL','ma']
#df['clasification']
y_values=df['num']
plt.bar(x_values,y_values)
plt.show()
plt.close("all")
#4. Dispositivos más vulnerables (Suma de servicios vulnerables y vulnerabilidades detectadas).
#5. Media de puertos abiertos frente a servicios inseguros y frente al total de servicios detectados.