import requests
import json
import pandas as pd
response=requests.get("https://cve.circl.lu/api/last").text
df=pd.read_json(response)
df=df.iloc[:10]
df=df.iloc[:,[0,1,3,6,7,9,10]]
print(df.to_html())
