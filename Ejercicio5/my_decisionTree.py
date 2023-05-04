from six import StringIO
from sklearn import tree
import pandas as pd
import pydotplus
from IPython.display import Image
from collections import Counter

def train(path):
    #df=pd.read_json("../json/devices_IA_clases.json")
    df = pd.read_json(path)
    X=df[["servicios","servicios_inseguros"]]
    y=df.peligroso
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X, y)
    return clf


def predict(path):
    clf=train(path)
    dfcheck = pd.read_json(path)
    arr1 = dfcheck.servicios
    arr2 = dfcheck.servicios_inseguros
    data = pd.DataFrame({'servicios': arr1, 'servicios_inseguros': arr2})
    return clf.predict(data)

def decision_tree_prediction(path, id, nserv, servIns):
    clf = train(path)
    arr1,arr2=[],[]
    arr1.append(nserv)
    arr2.append(servIns)
    data = pd.DataFrame({'servicios': arr1, 'servicios_inseguros': arr2})
    result = "El dispositivo " + id + (" es seguro" if clf.predict(data)== 0 else " es inseguro")
    return result

def grafica(path):
    clf=train(path)
    cols = ["servicios", "servicios_inseguros"]
    dot_data = StringIO()
    tree.export_graphviz(clf, out_file=dot_data,
                         filled=True, rounded=True,
                         special_characters=True, feature_names=cols, class_names=['0', '1'])
    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
    graph.write_png('static/images/decision_tree.png')
    return "static/images/decision_tree.png"

def result(path):
    arr=predict(path)
    counts = Counter(arr)
    print(f"Número de dispositivos seguros: {counts[0]}")
    print(f"Number de dispositivos peligrosos: {counts[1]}")


if __name__ == "__main__":
    result("devices_IA_clases.json")
    grafica("devices_IA_clases.json")



