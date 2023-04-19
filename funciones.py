import pandas as pd
import sqlite3
from IPython.core.display_functions import display
from IPython.display import HTML as a
import requests
from matplotlib import pyplot as plt
#VARIABLES GLOBALES:
#conexion= sqlite3.connect('pr1_SI.db')
#cur=conexion.cursor()
def obtenerTopIps(ntop, conexion):
    df=pd.read_sql_query("SELECT COUNT(*) as num, origen AS origen FROM ALERTS WHERE priority = 1 GROUP BY origen ORDER BY num desc",conexion)
    muestra=df[:ntop].copy()
    x_values=muestra['origen']
    y_values=muestra['num']
    plt.figure(num=None, figsize=(14, 6), dpi=80, facecolor='w', edgecolor='k')
    plt.bar(x_values,y_values)
    fichero="Top"+str(ntop)+"_ipsVuln"+".png"
    plt.savefig("static/images/"+fichero)
    return fichero
def obtenerTopDispositivos(ntop, conexion):
    df = pd.read_sql_query("SELECT (DETECT_VULNS+SERVICIOS_INS) suma, DEVICES_ID devices_id FROM ANALISIS ORDER BY suma DESC", conexion)
    muestra=df[:ntop].copy()
    plt.figure(num=None, figsize=(18, 10), dpi=80, facecolor='w', edgecolor='k')
    x_values = muestra["devices_id"]
    y_values = muestra["suma"]
    plt.bar(x_values, y_values)
    fichero="Top"+str(ntop)+"_vulnDev"+".png"
    plt.savefig("static/images/"+fichero)
    return fichero

def obtenerTopPeligrosos(ntop, peli, conexion):
    df = pd.read_sql_query("SELECT ID,devices_id, servicios, servicios_ins FROM ANALISIS ORDER BY servicios_ins desc", conexion)
    limit = 0
    describe = []
    for i, name in enumerate(df['devices_id']):
        danger = df['servicios_ins'][i]/df['servicios'][i]
        if danger > 0.3333:
           limit += 1
        elif math.isnan(danger):
            danger = 0
        describe.append((df['devices_id'][i], round(danger, 4)*100))
    x_values = []
    y_values = []
    describe.sort(key= lambda x: x[1], reverse=True)
    if peli == 1:
        i = 0
        while i < ntop and i < len(describe):
            tup = describe[i]
            if i < limit:
                x_values.append(tup[0])
                y_values.append(tup[1])
            i += 1
    else:
        i = limit
        while i < (ntop+limit) and i < len(describe):
            tup = describe[i]
            x_values.append(tup[0])
            y_values.append(tup[1])
            i += 1
    plt.figure(num=None, figsize=(18, 10), dpi=80, facecolor='w', edgecolor='k')
    plt.bar(x_values, y_values)
    plt.yticks(y_values)
    fichero="Top"+str(ntop)+"_dispPeli"+".png"
    plt.savefig("static/images/"+fichero)
    return fichero

def ej3():
    print("Ejercicio 3")
    response = requests.get("https://cve.circl.lu/api/last").text
    df = pd.read_json(response)
    df = df.iloc[:10]
    df = df.iloc[:, [0, 1, 3, 6, 7, 9, 10]]
    display(df)
    print(df.to_html())

if __name__ == "__main__":
    #checkeando el valor de __name__ prevenimos que se ejecute ej3() al ejecutar el archivo parte2.py
    ej3()

