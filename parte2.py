from reportlab.lib import colors, styles
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle

import json
import os
import requests
import pandas as pd
from flask import Flask, render_template, request, Response
from reportlab.lib.utils import ImageReader
import io

from reportlab.platypus import TableStyle, Table, SimpleDocTemplate, Paragraph

import funciones
import sqlite3
from flask import make_response
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape, A4
from reportlab.lib.units import inch
#from flask_weasyprint import HTML, render_pdf, CSS
from Ejercicio5 import my_linear_v2 as l
from Ejercicio5 import my_decisionTree as tree
from Ejercicio5 import my_randomforest as forest

conexion= sqlite3.connect('Practica1/pr1_SI.db', check_same_thread=False)
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
        p.drawCentredString(150, 50, "TITULO")
        if f1:
            p.drawCentredString(100, 600, "Top IPs:")
                # Add top IPs image
            top_ips_image = ImageReader("static/images/" + f1)
            p.drawImage(top_ips_image, x=200, y=400, width=5 * inch, height=3 * inch)

        if f2:
                # Add top devices image
            p.drawCentredString(100, 320, "Top Dispositivos:")
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
            p.drawString(100, 600, "Top IPs:")
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
    if not pdf:
        df = df.iloc[:, [0,1, 3,6, 10]]
        return render_template("ejercicio3.html", tables=[df.to_html()])
    elif pdf:
        df=df.iloc[:, [0, 1, 3, 6]]
        return df

@app.route('/ejercicio3/pdf', methods=['GET', 'POST'])
def pdf3_fixed_windows():
    df = ejercicio3(True)
    style_normal = ParagraphStyle(
        name='Normal',
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        leftIndent=0,
        rightIndent=0,
        firstLineIndent=0,
        alignment=TA_LEFT,
        spaceBefore=0,
        spaceAfter=0,
        bulletFontName='Helvetica',
        bulletFontSize=12,
        bulletIndent=0,
        textColor=colors.black,
        backColor=None,
        wordWrap=None,
        borderWidth=0,
        borderPadding=0,
        borderColor=None,
        borderRadius=None,
        allowWidows=1,
        allowOrphans=0,
        textTransform=None,
        endDots=None,
        splitLongWords=1,
        underlineWidth=0,
        underlineGap=None,
        strikeWidth=0,
        strikeGap=None,
        superScript=None,
        subScript=None,
    )
    data = [[Paragraph(str(cell), style_normal) for cell in row] for row in [df.columns.tolist()] + df.values.tolist()]
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
    table = Table(data, splitByRow=1)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    table.setStyle(style)
    doc.build([table])

    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

    buffer.close()

    return response


@app.route('/ejercicio5', methods=["GET", "POST"])
def ejercicio5():
    path= "Ejercicio5/devices_IA_clases.json"
    path2= "Ejercicio5/devices_IA_predecir_v2.json"

    if request.method == "POST":
        id = request.form['id']
        nServ = request.form['serv']
        nServIns=request.form['servin']
        op=request.form['option']
        #print((id, nServ, nServIns, op))
        if op == 'regresion_lineal':
            return render_template("ejercicio5.html", result=l.linear_prediction(path, path2,id, nServ, nServIns))
        elif op == 'decision_tree':
            return render_template("ejercicio5.html", result=tree.decision_tree_prediction(path, id, nServ, nServIns))
        elif op == 'random_forest':
            trees = int(request.form['trees'])
            return render_template("ejercicio5.html", result=forest.random_forest_prediction(path, id, nServ, nServIns, arbole=trees))
    elif request.method == "GET":
        return render_template("ejercicio5.html")
    tree.result(path)


@app.route('/ejercicio5json', methods=["GET", "POST"]) ### yamuestra el linear graph
def ejercicio5json():
    path = "Ejercicio5/devices_IA_clases.json"
    predict = "Ejercicio5/devices_IA_predecir_v2.json"
    if request.method == "POST":
        op=request.form['option']
        if op == 'regresion_lineal':
            print(l.createGraph(path, predict))
            return render_template("ejercicio5json.html", lineal=True, image=l.createGraph(path, predict)+".png")
        elif op == 'decision_tree':
            return render_template("ejercicio5json.html", result=tree.predict(path), tree=True)
        elif op == 'random_forest':
            trees = int(request.form['trees'])
            images = forest.generate_graph(path, arbole=trees)
            print(images)
            return render_template("ejercicio5json.html", result=forest.random_forest_prediction_json(path, predict, arbole=trees), forest=True, list=images)
    elif request.method == "GET":
        return render_template("ejercicio5json.html")

if __name__ == '__main__':
    app.run(debug=True)
