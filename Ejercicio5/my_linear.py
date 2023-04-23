import json

import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
## link: https://www.aprendemachinelearning.com/regresion-lineal-en-espanol-con-python/
data= pd.read_json("devices_IA_predecir.json") # open the data file
train_data= pd.read_json("devices_IA_clases.json")
#print(data.shape) # tenemos 35 disp con 3 vars
#print(data.head())
#print(data.describe()) #some statistics
#print(train_data.shape)
#print(train_data.head())
    #############################
#### Como tenemos que hablar de % de servicios inseguros, hemos de hacer analisis
# ####(serv_ins/serv)= [0,1] intervalo. Checkeamos si lo de 33% es vd.
######
#dataX=train_data[["servicios_inseguros"]]
#X_train=np.array(dataX)
train_data["division"]=(train_data["servicios_inseguros"]/train_data["servicios"]).fillna(0)
data["division"]=(train_data["servicios_inseguros"]/train_data["servicios"]).fillna(0)
#### Añadimos los campos de division para el porcentaje en ambos dataFrames.
X_train=np.array(train_data["division"]).reshape(-1,1)
y_train=train_data["peligroso"]
model=linear_model.LinearRegression() # Creamos el modelo de regresión lineal.
model.fit(X_train, y_train) # esto entrena el modelo con nuestras variables de entrenamiento (TAG peligroso && division para % ins)
print(model.coef_) # Es alto, gran correlacion.
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
#print(y_train)
#print(dataX)
