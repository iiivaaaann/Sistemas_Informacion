from subprocess import call

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import export_graphviz


def create_and_train_forest(path, arbole=7):
    if arbole > 1 and arbole < 16:
        dftrain = pd.read_json(path)
        #print(dftrain)
        clf = RandomForestClassifier(max_depth=2, random_state=0, n_estimators=arbole)
        data = dftrain[["servicios", "servicios_inseguros"]].to_numpy()
        #print(data)
        labels = dftrain["peligroso"]
        clf.fit(data, labels)
        return clf

def generate_graph(arbole=7):
    clf = create_and_train_forest(arbole)
    for i in range(len(clf.estimators_)):
        print(i)
        estimator = clf.estimators_[i]
        export_graphviz(estimator,
                        out_file='randtree.dot',
                        feature_names=['servicios', 'servicios_inseguros'],
                        class_names=['0', '1'],
                        rounded=True, proportion=False,
                        precision=2, filled=True)
        call(['dot', '-Tpng', 'randtree.dot', '-o', '../static/images/foresttree' + str(i) + '.png', '-Gdpi=600'])

def random_forest_prediction_json(path, arbole=7):
    dfpred = pd.read_json(path)
    model = create_and_train_forest(arbole)
    serv = dfpred.servicios
    servIns = dfpred.servicios_inseguros
    print(dfpred.servicios)
    df = pd.DataFrame({'servicios': serv, 'servicios_inseguros': servIns})
    pred = model.predict(df)
    return pred

def random_forest_prediction(path, id, serv, servIns, arbole=7):
    model = create_and_train_forest(path, arbole)
    result = "El dispositivo " + id + (" es seguro" if model.predict([[serv, servIns]]) == 0 else " es inseguro")
    return result

if __name__ == "__main__":
    print(random_forest_prediction("../json/devices_IA_predecir.json", "misterjagger", 8, 1))
    generate_graph(3)