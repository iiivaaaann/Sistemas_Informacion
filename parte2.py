
from flask import Flask, render_template

app = Flask(__name__, template_folder="templates")
@app.route('/')
def rootPage():
    return render_template("index.html")

@app.route('/ejercicio1')
def ejercicio1():
    print("Ejercicio 1")
    return render_template("ejercicio1.html")

@app.route('/ejercicio2')
def ejercicio2():
    print("Ejercicio 2")
    return render_template("ejercicio2.html")

@app.route('/ejercicio3')
def ejercicio3():
    print("Ejercicio 3")
    return render_template("ejercicio3.html")

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