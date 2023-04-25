import json
import os

import requests
import pandas as pd
from flask import Flask, render_template, request, Response
from reportlab.lib.utils import ImageReader
import io
import funciones
import sqlite3
from flask import make_response
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from flask_weasyprint import HTML, render_pdf, CSS
from Ejercicio5 import my_linear as l

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
        f1=f2=None
        if numIP:
            f1=funciones.obtenerTopIps(int(numIP), conexion)
        if numDisp:
            f2=funciones.obtenerTopDispositivos(int(numDisp), conexion)
        return render_template("ejercicio1.html", numIP=numIP, numDisp=numDisp, f1=f1, f2=f2)
    elif request.method == "GET":
        return render_template("ejercicio1.html")
@app.route('/ejercicio1/pdf', methods=['GET', 'POST'])
def pdf1():
    if request.method == "POST":
        numIP = request.form['numIP']
        numDisp = request.form['numDisp']
        f1=f2=None
        if numIP:
            f1=funciones.obtenerTopIps(int(numIP), conexion)
        if numDisp:
            f2=funciones.obtenerTopDispositivos(int(numDisp), conexion)

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        if f1:
                #p.drawString(100, 600, "Top IPs:")
                # Add top IPs image
            top_ips_image = ImageReader("static/images/" + f1)
            p.drawImage(top_ips_image, x=200, y=400, width=5 * inch, height=3 * inch)
        if f2:
                # Add top devices image
            top_devices_image = ImageReader("static/images/" + f2)
            p.drawImage(top_devices_image, x=50, y=50, width=7 * inch, height=3.5 * inch)
        p.showPage()
        p.save()
        buffer.seek(0)
        response = make_response(buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
        return response
    elif request.method == "GET":
        return render_template("ejercicio1.html")

@app.route('/ejercicio2', methods=['GET', 'POST'])
def ejercicio2():
    print("Ejercicio 2")
    if request.method == "POST":
        numDisp = int(request.form['numDisp'])
        peli = int(request.form['peli'])
        f1 = funciones.obtenerTopPeligrosos(numDisp, peli, conexion)
        return render_template("ejercicio2.html", peli=peli, f1=f1)
    elif request.method == "GET":
        return render_template("ejercicio2.html")
@app.route('/ejercicio2/pdf', methods=['GET', 'POST'])
def pdf2():
    if request.method == "POST":
        numDisp = int(request.form['numDisp'])
        peli = int(request.form['peli'])
        f1 = funciones.obtenerTopPeligrosos(numDisp, peli, conexion)
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        if f1:
            # p.drawString(100, 600, "Top IPs:")
            # Add top IPs image
            top_ips_image = ImageReader("static/images/" + f1)
            p.drawImage(top_ips_image, x=200, y=400, width=5 * inch, height=3 * inch)

        p.showPage()
        p.save()
        buffer.seek(0)
        response = make_response(buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
        return response
    elif request.method == "GET":
        return render_template("ejercicio2.html")
@app.route('/ejercicio3')
def ejercicio3(pdf=False):
    print("Ejercicio 3")
    response = requests.get("https://cve.circl.lu/api/last/10").text
    df = pd.read_json(response)
    df = df.iloc[:10]
    df = df.iloc[:, [0, 1, 3, 6, 7, 9, 10]]
    if not pdf:
        return render_template("ejercicio3.html", tables=[df.to_html()])
    elif pdf:
        return df.to_html()
@app.route('/ejercicio3/pdf', methods=['GET', 'POST'])
def pdf3():
    css = CSS(string='''
           @page { size: A4 landscape; margin: 0cm }
           table.dataframe { border-collapse: collapse; }
           table.dataframe th, table.dataframe td {
               border: 1px solid black;
               padding: 5px;
               text-align: center;
           }
           .chart-container { border: 1px solid #ccc; padding: 10px; }
           .chart-title { font-size: 20px; font-weight: bold; text-align: center; }
           .chart-axis-label { font-size: 14px; font-weight: bold; }
           .chart-axis-tick { font-size: 12px; }
       ''')
    pdf=HTML(string=ejercicio3(True)).write_pdf(stylesheets=[css])
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
    return response




@app.route('/ejercicio5', methods=["GET", "POST"])
def ejercicio5():
    path="json/devices_IA_clases.json"
    if request.method == "POST":
        id = request.form['id']
        nServ = request.form['serv']
        nServIns=request.form['servin']
        op=request.form['option']
        #print((id, nServ, nServIns, op))
        if op == 'regresion_lineal':
            return render_template("ejercicio5.html", result=l.linear_prediction(path,id, nServ, nServIns))
        elif op == 'decision_tree':
            return render_template("ejercicio5.html", result=l.linear_prediction(path, id, nServ, nServIns))
    elif request.method == "GET":
        return render_template("ejercicio5.html")

if __name__ == '__main__':
    app.run(debug=True)
