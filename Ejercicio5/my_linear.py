import json
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd


def create_and_train_Linear(path):
    #data= pd.read_json("devices_IA_predecir.json") # open the data file
    train_data= pd.read_json(path)
    train_data["division"]=(train_data["servicios_inseguros"]/train_data["servicios"]).fillna(0)
    #data["division"]=(train_data["servicios_inseguros"]/train_data["servicios"]).fillna(0)
    X_train=np.array(train_data["division"]).reshape(-1,1)
    y_train=train_data["peligroso"]
    model=linear_model.LinearRegression()
    model.fit(X_train, y_train)
    return model

def predict(id, nserv, servIns, model):
    n_json = [{
        "id": id,
        "servicios": nserv,
        "servicios_inseguros": servIns
    }]
    js_str = json.dumps(n_json)
    jso = pd.read_json(js_str)
    jso["division"] = jso["servicios_inseguros"] / jso["servicios"]
    X_jso = np.array(jso["division"]).reshape(-1, 1)
    n_pred = model.predict(X_jso)
    return n_pred

def linear_prediction(path, id, nserv, servIns):
    model=create_and_train_Linear(path)
    pred=predict(id, nserv, servIns, model)
    dec_umbral = 0.5
    y_pred_umbralizado = [1 if y >= dec_umbral else 0 for y in pred]
    result="El dispositivo " + id + (" es seguro" if y_pred_umbralizado[0] == 0 else " es inseguro")
    return result

if __name__ == '__main__':
    print(linear_prediction("juanpedro", 10, 2))
################this is test code, wont be used.###########################
''''
# procedemos a predecir:
X_pred= np.array(data["division"]).reshape(-1,1)
y_pred=model.predict(X_pred)
print(y_pred) # Esto nos da valores que no son 0 o 1 exactamente, por tanto, ponemos un "umbral de decision"
dec_umbral=0.5 # si > umbral, es 1, si no es 0.
y_pred_umbralizado=[1 if y>=dec_umbral else 0 for y in y_pred]
print(y_pred_umbralizado)
n_json=[{
        "id": "sanpedro_tehackea",
        "servicios": 3,
        "servicios_inseguros": 1
        }]
js_str= json.dumps(n_json)
print(js_str)
jso=pd.read_json(js_str)
jso["division"]=jso["servicios_inseguros"]/jso["servicios"]
X_jso=np.array(jso["division"]).reshape(-1,1)
n_pred=model.predict(X_jso)
n_pred_umbralizado=[1 if y>=dec_umbral else 0 for y in n_pred]
for i in range(len(n_pred_umbralizado)):
    print("El dispositivo "+ str(jso.iloc[i]["id"]) + (" es seguro" if n_pred_umbralizado[0]==0 else " es inseguro"))
'''
