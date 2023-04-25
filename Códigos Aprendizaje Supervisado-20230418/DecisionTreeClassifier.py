from sklearn import tree
from sklearn.datasets import load_iris
import graphviz #https://graphviz.org/download/
import pandas as pd
import pandas as pd

from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics

def train():
    df=pd.read_json("../JSON Ejercicios IA 202223-20230418/devices_IA_clases.json")
    X=df[["servicios","servicios_inseguros"]]
    y=df.peligroso
    print(X)
    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X, y)
    # Predict
    data=pd.DataFrame({'servicios':[3,2], 'servicios_inseguros':[0,1]})
    print(clf.predict(data))
    # Print plot


train()

