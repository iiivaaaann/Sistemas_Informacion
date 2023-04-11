
from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello_world():
    return '<h1>Hello, World! <ul><li>Hola juan</li></ul></h1>'

def ejer2():
    print("Ejer 2")

def ejer3():
    print("Ejer 3")

def ejer4():
    print("Ejer 4")

def ejer5():
    print("Ejer 5")


if __name__ == '__main__':
    app.run(debug=True)