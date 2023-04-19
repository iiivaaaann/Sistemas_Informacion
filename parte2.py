import pdfkit
import requests
import pandas as pd
from flask import Flask, render_template, request, send_file, make_response, Response
import funciones
import sqlite3
from xhtml2pdf import pisa
from api2pdf import Api2Pdf
API2PDF_API_KEY='5a12d7c8-9255-47a1-aaf9-a73ead097999'
USERAGENT = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
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

@app.route('/ejercicio2')
def ejercicio2():
    print("Ejercicio 2")
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
        return Response(df.to_html())


@app.route('/ejercicio4')
def ejercicio4(): ## Para usar esto es necesario instalar wkhtmltopdf con sudo apt-get o brew. para windows buscar xd ; de momento solo genera el pdf del ejercicio 3
    html = ejercicio3(True).data.decode('utf-8')
    pdf = pdfkit.from_string(html, False, options={'quiet': ''})
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"
    return response

@app.route('/ejercicio5')
def ejercicio5():
    print("Ejercicio 5")
    return render_template("ejercicio5.html")

if __name__ == '__main__':
    app.run(debug=True)