import json

from sklearn import linear_model
from sklearn.model_selection import train_test_split
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
path = "devices_IA_clases.json"
predict = "devices_IA_predecir_v2.json"
def createTrainedModel(path, path2):
    train_File= pd.read_json(path)
    test_file= pd.read_json(path2)
    X_train= np.array((train_File["servicios_inseguros"]/train_File["servicios"]).fillna(0)).reshape(-1,1)
    y_train= np.array(train_File["peligroso"]).reshape(-1,1)
    #X_train, X_test, y_train, y_test= train_test_split(X_data, y_data, test_size=0.3)
    X_test= np.array((test_file["servicios_inseguros"]/test_file["servicios"]).fillna(0)).reshape(-1,1)
    y_test= np.array(test_file["peligroso"]).reshape(-1,1)
    model= linear_model.LinearRegression()
    model.fit(X_train, y_train)
    return model, X_test, y_test

def createGraph():
    model, X_test, y_test= createTrainedModel("devices_IA_clases.json", "devices_IA_predecir_v2.json")
    y_pred= model.predict(X_test)
    plt.scatter(X_test,y_test,color="black")
    plt.plot(X_test, y_pred, color="red", linewidth=3)
    plt.xticks(())
    plt.yticks(())
    fichero="regr_graph"
    plt.savefig("../static/images/"+fichero)
    return "static/images/"+fichero

def predict(id, nserv, servIns, model):
    n_json = [{
        "id": id,
        "servicios": nserv,
        "servicios_inseguros": servIns
    }]
    js_str = json.dumps(n_json)
    jso = pd.read_json(js_str)
    jso["division"] = (jso["servicios_inseguros"] / jso["servicios"]).fillna(0)
    X_jso = np.array(jso["division"]).reshape(-1, 1)
    n_pred = model.predict(X_jso)
    return n_pred

def linear_prediction(path, path2, id, nserv, servIns):
    model, useless1, useless2=createTrainedModel(path, path2)
    pred=predict(id, nserv, servIns, model)
    dec_umbral = 0.5
    y_pred_umbralizado = [1 if y >= dec_umbral else 0 for y in pred]
    result="El dispositivo " + id + (" es seguro" if y_pred_umbralizado[0] == 0 else " es inseguro")
    return result


if __name__ == '__main__':
   ## model, X_test, y_test = createTrainedModel()
    createGraph()