from six import StringIO
from sklearn import tree
import pandas as pd
import pydotplus
from IPython.display import Image
from collections import Counter

def train():
    df=pd.read_json("../json/devices_IA_clases.json")
    X=df[["servicios","servicios_inseguros"]]
    y=df.peligroso
    print(X)
    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X, y)
    return clf


def predict():
    clf=train()
    dfcheck = pd.read_json("../json/devices_IA_predecir.json")
    arr1 = dfcheck.servicios
    arr2 = dfcheck.servicios_inseguros
    data = pd.DataFrame({'servicios': arr1, 'servicios_inseguros': arr2})
    return clf.predict(data)

def grafica():
    clf=train()
    cols = ["servicios", "servicios_inseguros"]
    dot_data = StringIO()
    tree.export_graphviz(clf, out_file=dot_data,
                         filled=True, rounded=True,
                         special_characters=True, feature_names=cols, class_names=['0', '1'])
    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
    graph.write_png('disposivtos.png')
    Image(graph.create_png())
def result():
    arr=predict()
    # Use Counter to count the number of occurrences of each element
    counts = Counter(arr)
    # Print the results
    print(f"Número de dispositivos seguros: {counts[0]}")
    print(f"Number of 1s: {counts[1]}")

if __name__ == "__main__":
    train()


