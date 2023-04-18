import requests
import pandas as pd
from flask import Flask, render_template, request
import funciones
import sqlite3
from IPython.display import HTML


conexion= sqlite3.connect('pr1_SI.db', check_same_thread=False)
cur=conexion.cursor()

app = Flask(__name__, template_folder="templates")
@app.route('/')
def rootPage():
    return render_template("index.html")

@app.route('/ejercicio1', methods=["GET", "POST"])
def ejercicio1():
    print("Ejercicio 1")
    if request.method == "POST":
        numIP = request.form['numIP']
        numDisp = request.form['numDisp']
        f1=funciones.obtenerTopIps(int(numIP), conexion)
        f2=funciones.obtenerTopDispositivos(int(numDisp), conexion)
        return render_template("ejercicio1.html", numIP=numIP, numDisp=numDisp, f1=f1, f2=f2)
    elif request.method == "GET":
        return render_template("ejercicio1.html")

@app.route('/ejercicio2')
def ejercicio2():
    print("Ejercicio 2")
    return render_template("ejercicio2.html")

@app.route('/ejercicio3')
def ejercicio3():
    print("Ejercicio 3")
    response = requests.get("https://cve.circl.lu/api/last/10").text
    df = pd.read_json(response)
    df = df.iloc[:10]
    df = df.iloc[:, [0, 1, 3, 6, 7, 9, 10]]
    return render_template("ejercicio3.html", tables=[df.to_html()])

@app.route('/ejercicio4')
def ejercicio4():
    print("Ejercicio 4")
    return render_template("ejercicio4.html")

@app.route('/ejercicio5')
def ejercicio5():
    print("Ejercicio 5")
    return render_template("ejercicio5.html")

if __name__ == '__main__':
    app.run(debug=True)