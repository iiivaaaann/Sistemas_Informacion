import pandas as pd
import sqlite3
import json
import matplotlib.pyplot as plt
import numpy as np


#VARIABLES GLOBALES:
conexion= sqlite3.connect('pr1_SI.db')
cur=conexion.cursor()

#def model_creation()
#CREATE TAB ALERTS
def createChartModel():
    cur.execute("DROP TABLE IF EXISTS ALERTS")
    cur.execute("CREATE TABLE IF NOT EXISTS ALERTS (ID integer PRIMARY KEY autoincrement,TIME TIMESTAMP, SID INT, MSG TEXT, CLASIFICATION TEXT, PRIORITY INT,PROTOCOLO TEXT, ORIGEN TEXT, DESTINO TEXT, PUERTO INT)")
    cur.execute("CREATE TABLE if not exists RESPONSABLE (nombre text PRIMARY KEY, telefono int, rol text)")
    cur.execute("CREATE TABLE if not exists DEVICES (id text primary key , ip text, responsable_nombre text, localizacion text, FOREIGN KEY (responsable_nombre) references responsable(nombre))")
    cur.execute("CREATE TABLE if not exists ANALISIS (ID INTEGER PRIMARY KEY autoincrement, devices_id text UNIQUE, servicios int, servicios_ins int, detect_vulns int, FOREIGN KEY (devices_id) references DEVICES(id))")
    cur.execute("CREATE TABLE if not exists PUERTOS (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre text,analisis_id int NOT NULL, FOREIGN KEY (analisis_id) REFERENCES ANALISIS(id) CONSTRAINT NOT_REPEATED_PORTS_ANALISIS UNIQUE (nombre, analisis_id))")

def insertInformationFromFiles():
    csvData=pd.read_csv("alerts.csv", sep=',', parse_dates=True)
    dataFrame=pd.DataFrame(csvData)
    for row in dataFrame.itertuples():
        cur.execute("INSERT INTO ALERTS (TIME, SID, MSG, CLASIFICATION, PRIORITY, PROTOCOLO, ORIGEN, DESTINO, PUERTO) VALUES (?,?,?,?,?,?,?,?,?)", (row[1], row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]))
    print("Alerts.csv insertado con éxito en tabla ALERTS.\n\nInsertando devices.json en tablas del modelo:\n\n")
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
           loc=None if i["localizacion"]=="None" else i["localizacion"]
           cur.execute("INSERT OR IGNORE INTO DEVICES (id, IP, localizacion, responsable_nombre) VALUES (?,?,?,?)",(i["id"], i["ip"],loc,i["responsable"]["nombre"]))
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
            print("Device id: " + i["id"])
            print("Analisis id: " + str(cur.execute("SELECT ID FROM ANALISIS WHERE DEVICES_ID=?", (i["id"],)).fetchall()[0][0]))
            print("Puertos abiertos: " + str(i["analisis"]["puertos_abiertos"]))
            analisis_id=cur.execute("SELECT ID FROM ANALISIS WHERE DEVICES_ID=?", (i["id"],)).fetchall()[0][0]
            for j in i["analisis"]["puertos_abiertos"]:
                if i["analisis"]["puertos_abiertos"]!="None":
                    name=j
                    print("nombre: " + name + " id analisis: " + str(analisis_id))
                    cur.execute("INSERT OR IGNORE INTO PUERTOS (NOMBRE, ANALISIS_ID) VALUES (?,?)",(name,analisis_id))
        print(".... puertos insertados correctamente!")


    conexion.commit()


#Ejer 2
def ejercicio2():
#1. Número de dispositivos
#Basando en IPs diferentes
    df=pd.read_sql_query("SELECT DISTINCT origen FROM ALERTS UNION SELECT DISTINCT destino FROM ALERTS ",conexion)
    print("Número de dispotivos = " + str(df.size) + " dispostivos")
    df=pd.read_sql_query("SELECT COUNT(*) NDEV FROM DEVICES", conexion)
    print("Tenemos " + str(df["NDEV"][0]) + " dispositivos conocidos")
    # como nos piden los none y los missing:

    df=pd.read_sql_query("select count(*) as MISSING_MSGS from ALERTS where msg like '%issing%'", conexion)
    print("Tenemos "+str(df["MISSING_MSGS"][0]) + " alertas con valores MISSING en sus mensajes")

    df1=pd.read_sql_query("SELECT * FROM DEVICES", conexion)
    df2=pd.read_sql_query("SELECT * FROM ANALISIS",conexion)
    df3=pd.read_sql_query("SELECT * FROM PUERTOS",conexion)
    df4=pd.read_sql_query("SELECT * FROM RESPONSABLE", conexion)

    print("Mostrando \"NONES\" del esquema generado desde devices.json:")
    print("TABLA DEVICES:")
    print(df1.isnull().sum(), end='\n\n')
    print("TABLA ANALISIS:")
    print(df2.isnull().sum(), end='\n\n')
    print("TABLA PUERTOS:")
    print(df3.isnull().sum(), end='\n\n')
    print("TABLA RESPONSABLES:")
    print(df4.isnull().sum(), end='\n\n')



    #2. Número de alertas

    df=pd.read_sql_query("SELECT sid FROM ALERTS ",conexion)
    print("Número de alertas = " + str(df.size) + " alertas")

    #3. Media y desviación estándar del totla de puertos abiertos
    #df=pd.read_sql_query("SELECT puerto FROM ALERTS ",conexion)

    #print("Media = " + str(df.mean()) )
    #print("Desviación estándar = " + str(df.std()))
    df=pd.read_sql_query("SELECT COUNT(*) P_ABIERTOS, ANALISIS_ID FROM PUERTOS GROUP BY ANALISIS_ID", conexion)
    print("El número medio de puertos abiertos en los dispositivos es: "+str(df["P_ABIERTOS"].mean())+" puertos.")
    print("La desviación estándar de puertos abiertos es : "+ str(round(df["P_ABIERTOS"].std(),2)))

    #4. Media y desviación est´andar del número de servicios inseguros detectados
    df=pd.read_sql_query("SELECT sum(SERVICIOS_INS) SERV_INSEGUROS, ID FROM ANALISIS GROUP BY ID", conexion)
    print("El número medio de servicios inseguros en los dispositivos es: "+str(round(df["SERV_INSEGUROS"].mean(),2))+" servicios.")
    print("La desviación estándar de servicios inseguros en los dispositivos es: "+str(round(df["SERV_INSEGUROS"].std(),2))+" servicios.")

    #5. Media y desviación estándar del número de vulnerabilidades detectadas.
    df=pd.read_sql_query("SELECT SUM(DETECT_VULNS) VULNS, ID FROM ANALISIS GROUP BY ID", conexion)
    print("El número medio de vulnerabilidades detectadas en los dispositivos es: "+str(round(df["VULNS"].mean(),2))+" vulnerabilidades.")
    print("La desviación estándar de vulnerabilidades detectadas en los dispositivos es: "+str(round(df["VULNS"].std(),2))+" vulnerabilidades.")


    #6. Valor mínimo y valor máximo del total de puertos abiertos. (Consulta un poco compleja por la estructura de la T puertos)
    df=pd.read_sql_query("SELECT MAX(PUERTOS_ABIERTOS), ANALISIS_ID FROM (SELECT COUNT(*) AS PUERTOS_ABIERTOS, ANALISIS_ID FROM PUERTOS GROUP BY ANALISIS_ID)", conexion)
    print("Como máximo hay "+ str(df["MAX(PUERTOS_ABIERTOS)"][0]) + " puertos abiertos correspondientes al id de análisis: " + str(df["ANALISIS_ID"][0])
          +" y al dispositivo: "+ str(pd.read_sql_query("SELECT ID FROM DEVICES WHERE ID= (SELECT DEVICES_ID FROM ANALISIS WHERE ID=?)",conexion, params=[str(df["ANALISIS_ID"][0])])["id"][0]))
    df=pd.read_sql_query("SELECT MIN(PUERTOS_ABIERTOS), ANALISIS_ID FROM (SELECT COUNT(*) AS PUERTOS_ABIERTOS, ANALISIS_ID FROM PUERTOS GROUP BY ANALISIS_ID)", conexion)
    print("Como mínimo hay "+ str(df["MIN(PUERTOS_ABIERTOS)"][0]) + " puertos abiertos correspondientes al id de análisis: " + str(df["ANALISIS_ID"][0]) +
        " y al dispositivo: "+ str(pd.read_sql_query("SELECT ID FROM DEVICES WHERE ID= (SELECT DEVICES_ID FROM ANALISIS WHERE ID=?)",conexion, params=[str(df["ANALISIS_ID"][0])])["id"][0]))


    #7. Valor mínimo y valor máximo del número de vulnerabilidades detectadas.
    df=pd.read_sql_query("SELECT DETECT_VULNS FROM ANALISIS", conexion)
    print("Podemos encontrar un mínimo de: " + str(df.min()[0])+" vulnerabilidades detectadas.")
    print("Podemos encontrar un máximo de: " + str(df.max()[0])+" vulnerabilidades detectadas.")



#Ejer 3
def ejercicio3():
    print("Ejercicio 3. Agrupamos según mes y según prioridad de alerta")
    #Agrupar de forma separada; por prioridad de alerta (1 al 3, de grave a leve), y por fechas (mes de julio o mes de agosto)
    #Según cada agrupación, mostrar con respecto a vulnerabilidades detectadas en los dispositivos (que puede ser origen o destino):
    df = pd.read_sql_query("SELECT STRFTIME('%Y-%m', time) AS year_month, COUNT(*) time, priority from alerts GROUP BY STRFTIME('%Y-%m', time), priority", conexion)
    #1. Número de observaciones
    print("Mes de Julio, número de alertas bajas: " + str(df["time"][0]))
    print("Mes de Julio, número de alertas medias: " + str(df["time"][1]))
    print("Mes de Julio, número de alertas altas: " + str(df["time"][2]))
    print("Mes de Agosto, número de alertas bajas: " + str(df["time"][3]))
    print("Mes de Agosto, número de alertas medias: " + str(df["time"][4]))
    print("Mes de Agosto, número de alertas altas: " + str(df["time"][5]))

    #2. Número de valores ausentes
    df=pd.read_sql_query("select count(*) as MISSING_MSGS, STRFTIME('%Y-%m', time) as year_month, priority from ALERTS where msg like '%issing%' group by priority, STRFTIME('%Y-%m', time)", conexion)
    print("Todos los valores ausentes encontrados son de prioridad 3")
    print("Mes de Julio, " +str(df["MISSING_MSGS"][0])+" valores ausentes encontrados")
    print("Mes de Agosto, " +str(df["MISSING_MSGS"][1])+" valores ausentes encontrados")

    #3. Mediana
    #Como el dispositivo puede ser el origen o el destino, se contará como vulnerabilidad detectada si aparece en la alerta en el origen o en el destino
    #Pero hay que seguir dividiendo entre mes de julio y agosto, y prioridades. Chequear el código
    df = pd.read_sql_query("select count(*)  as vulnPerDevice, origen from (select origen, STRFTIME('%Y-%m', time) as year_month, priority from alerts union all select destino, STRFTIME('%Y-%m', time) as year_month, priority from alerts) where year_month is '2022-07' or '2022-08' group by origen", conexion)
    datata = df.describe()
    print("Sobre los datos descubiertos de las vulnerabilidades según los dispositivos:")
    print("Mediana: " + str(int(datata["vulnPerDevice"][5])), end="\t")
    #4. Media
    print("Media: " + str(round(datata["vulnPerDevice"][1], 3)), end="\t")
    #5. Varianza
    print("Varianza: " + str(round(pow(datata["vulnPerDevice"][2], 2), 3)))
    #6. Máximo y mínimo
    print("Máximo: " + str(int(datata["vulnPerDevice"][7])), end="\t")
    print("Mínimo: " + str(int(datata["vulnPerDevice"][3])))
    #Falta imprimir estos valores agrupando por mes y por prioridad de alerta
    df = pd.read_sql_query("select count(*) as vulnPerDevice, origen, year_month, priority from(select origen, STRFTIME('%Y-%m', time) as year_month, priority from alerts union all select destino, STRFTIME('%Y-%m', time) as year_month, priority from alerts) where year_month is '2022-07' and priority is 1 group by origen, year_month", conexion)
    print("Sobre alertas en julio, con prioridad 1:")
    datata = df.describe()
    print("Mediana: " + str(int(datata["vulnPerDevice"][5])), end="\t")
    # 4. Media
    print("Media: " + str(round(datata["vulnPerDevice"][1], 3)), end="\t")
    # 5. Varianza
    print("Varianza: " + str(round(pow(datata["vulnPerDevice"][2], 2), 3)))
    # 6. Máximo y mínimo
    print("Máximo: " + str(int(datata["vulnPerDevice"][7])), end="\t")
    print("Mínimo: " + str(int(datata["vulnPerDevice"][3])))
    df = pd.read_sql_query(
        "select count(*) as vulnPerDevice, origen, year_month, priority from(select origen, STRFTIME('%Y-%m', time) as year_month, priority from alerts union all select destino, STRFTIME('%Y-%m', time) as year_month, priority from alerts) where year_month is '2022-07' and priority is 2 group by origen, year_month",
        conexion)
    print("Sobre alertas en julio, con prioridad 2:")
    datata = df.describe()
    print("Mediana: " + str(int(datata["vulnPerDevice"][5])), end="\t")
    # 4. Media
    print("Media: " + str(round(datata["vulnPerDevice"][1], 3)), end="\t")
    # 5. Varianza
    print("Varianza: " + str(round(pow(datata["vulnPerDevice"][2], 2), 3)))
    # 6. Máximo y mínimo
    print("Máximo: " + str(int(datata["vulnPerDevice"][7])), end="\t")
    print("Mínimo: " + str(int(datata["vulnPerDevice"][3])))
    df = pd.read_sql_query(
        "select count(*) as vulnPerDevice, origen, year_month, priority from(select origen, STRFTIME('%Y-%m', time) as year_month, priority from alerts union all select destino, STRFTIME('%Y-%m', time) as year_month, priority from alerts) where year_month is '2022-07' and priority is 3 group by origen, year_month",
        conexion)
    print("Sobre alertas en julio, con prioridad 3:")
    datata = df.describe()
    print("Mediana: " + str(int(datata["vulnPerDevice"][5])), end="\t")
    # 4. Media
    print("Media: " + str(round(datata["vulnPerDevice"][1], 3)), end="\t")
    # 5. Varianza
    print("Varianza: " + str(round(pow(datata["vulnPerDevice"][2], 2), 3)))
    # 6. Máximo y mínimo
    print("Máximo: " + str(int(datata["vulnPerDevice"][7])), end="\t")
    print("Mínimo: " + str(int(datata["vulnPerDevice"][3])))
    df = pd.read_sql_query(
        "select count(*) as vulnPerDevice, origen, year_month, priority from(select origen, STRFTIME('%Y-%m', time) as year_month, priority from alerts union all select destino, STRFTIME('%Y-%m', time) as year_month, priority from alerts) where year_month is '2022-08' and priority is 1 group by origen, year_month",
        conexion)
    print("Sobre alertas en agosto, con prioridad 1:")
    datata = df.describe()
    print("Mediana: " + str(int(datata["vulnPerDevice"][5])), end="\t")
    # 4. Media
    print("Media: " + str(round(datata["vulnPerDevice"][1], 3)), end="\t")
    # 5. Varianza
    print("Varianza: " + str(round(pow(datata["vulnPerDevice"][2], 2), 3)))
    # 6. Máximo y mínimo
    print("Máximo: " + str(int(datata["vulnPerDevice"][7])), end="\t")
    print("Mínimo: " + str(int(datata["vulnPerDevice"][3])))
    df = pd.read_sql_query(
        "select count(*) as vulnPerDevice, origen, year_month, priority from(select origen, STRFTIME('%Y-%m', time) as year_month, priority from alerts union all select destino, STRFTIME('%Y-%m', time) as year_month, priority from alerts) where year_month is '2022-08' and priority is 2 group by origen, year_month",
        conexion)
    print("Sobre alertas en julio, con prioridad 2:")
    datata = df.describe()
    print("Mediana: " + str(int(datata["vulnPerDevice"][5])), end="\t")
    # 4. Media
    print("Media: " + str(round(datata["vulnPerDevice"][1], 3)), end="\t")
    # 5. Varianza
    print("Varianza: " + str(round(pow(datata["vulnPerDevice"][2], 2), 3)))
    # 6. Máximo y mínimo
    print("Máximo: " + str(int(datata["vulnPerDevice"][7])), end="\t")
    print("Mínimo: " + str(int(datata["vulnPerDevice"][3])))
    df = pd.read_sql_query(
        "select count(*) as vulnPerDevice, origen, year_month, priority from(select origen, STRFTIME('%Y-%m', time) as year_month, priority from alerts union all select destino, STRFTIME('%Y-%m', time) as year_month, priority from alerts) where year_month is '2022-08' and priority is 3 group by origen, year_month",
        conexion)
    print("Sobre alertas en julio, con prioridad 3:")
    datata = df.describe()
    print("Mediana: " + str(int(datata["vulnPerDevice"][5])), end="\t")
    # 4. Media
    print("Media: " + str(round(datata["vulnPerDevice"][1], 3)), end="\t")
    # 5. Varianza
    print("Varianza: " + str(round(pow(datata["vulnPerDevice"][2], 2), 3)))
    # 6. Máximo y mínimo
    print("Máximo: " + str(int(datata["vulnPerDevice"][7])), end="\t")
    print("Mínimo: " + str(int(datata["vulnPerDevice"][3])))

#Ejer 4
def ejercicio4(): #Falta el ultimo apartado.
    #1. Mostrar las 10 IP de origen más problemáticas, representadas en un gráfico de barras (las IPs de origen más problemáticas son las que más alertas han generado con prioridad 1).
    #df=pd.read_sql_query("SELECT COUNT(*) as num, origen FROM ALERTS WHERE priority = 1 GROUP BY origen ORDER BY num desc",conexion)
    df=pd.read_sql_query("SELECT COUNT(*) as num, origen AS origen FROM ALERTS WHERE priority = 1 GROUP BY origen ORDER BY num desc",conexion)
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
    df=pd.read_sql_query("SELECT time as time FROM ALERTS ",conexion)
    df.index=df['time']
    print(df)
    #3. Número de alertas por categoría, representadas en un gráfico de barras.
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
    df=pd.read_sql_query("SELECT (DETECT_VULNS+SERVICIOS_INS) suma, DEVICES_ID devices_id FROM ANALISIS", conexion)
    print(df)
    plt.figure(num=None, figsize=(18, 10), dpi=80, facecolor='w', edgecolor='k')
    x_values=df["devices_id"]
    y_values=df["suma"]
    plt.bar(x_values, y_values)
    plt.show()
    plt.close("all")
    #5. Media de puertos abiertos frente a servicios inseguros y frente al total de servicios detectados.
    # Consideramos que "frente" se refiere a proporción?
    df=pd.read_sql_query("SELECT devices_id, servicios_ins,detect_vulns FROM ANALISIS", conexion)
    df2= pd.read_sql_query("SELECT COUNT(*) P_ABIERTOS, ANALISIS_ID FROM PUERTOS GROUP BY ANALISIS_ID", conexion)
    n=len(df.index)
    x=np.arange(n)
    width=0.25
    plt.bar(x-width,df['servicios_ins'],width=width,label="servicios_ins")
    plt.bar(x,df['detect_vulns'],width=width,label="detect_vulns")
    plt.xticks(x,df.index)
    plt.legend(loc='best')
    plt.show()
    plt.close("all")

###################################
#       Falta: 4.2, 4.5           #
###################################

if __name__ == '__main__':
    print("Creando modelo de tablas:")
    createChartModel()
    insertInformationFromFiles()
    print("Resolviendo ejercicio 2:")
    ejercicio2()
    print("Resolviendo ejercicio 3:")
    ejercicio3()
    print("Resolviendo ejercicio 4:")
    ejercicio4()
    conexion.close()
    exit(0)