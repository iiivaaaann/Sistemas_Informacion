from six import StringIO
from sklearn import tree
import pandas as pd
import pydotplus
from IPython.display import Image
import sklearn.externals

def train():
    df=pd.read_json("../JSON Ejercicios IA 202223-20230418/devices_IA_clases.json")
    cols=["servicios","servicios_inseguros"]
    X=df[["servicios","servicios_inseguros"]]
    y=df.peligroso
    print(X)
    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X, y)
    # Predict
    arr1=df.servicios
    arr2=df.servicios_inseguros
    data=pd.DataFrame({'servicios':arr1, 'servicios_inseguros':arr2})
    print(clf.predict(data))
    # Print plot

    dot_data = StringIO()
    tree.export_graphviz(clf, out_file=dot_data,
                filled=True, rounded=True,
                special_characters=True,feature_names = cols,class_names=['0','1'])
    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
    graph.write_png('disposivtos.png')
    Image(graph.create_png())


train()

