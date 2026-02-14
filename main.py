#main.py
from fastapi import FastAPI , Request
import requests
import json
import  os
from typing import Annotated
app= FastAPI()

#Abrir el archivo de configuración
from pathlib import Path
ruta_base = Path(__file__).parent 
#archivo_ruta = ruta_base.parent / "config.json"
archivo_ruta = ruta_base / "config.json"
with open(archivo_ruta, 'r') as f:
    data = json.load(f) # Lee y convierte a diccionario en un solo paso
    url_token_wms = data["items"][0]["url_token_wms"]
    usr_id_wms    = data["items"][0]["usr_id_wms"]
    password_wms  = data["items"][0]["password_wms"]
    url_wms_item  = data["items"][0]["url_wms_item"]

# La API que queremos consumir para el token
url = url_token_wms
# The token parameters required by the API
raw_data = f'{{"usr_id": "{usr_id_wms}", "password": "{password_wms}"}}'

headers = {"Content-Type": "application/json"}


@app.get("/items")

def obtener_datos_externos(warehouseId: str, itemNumber: str, request: Request):
    # 1. Consumir la API externa usando requests
    response = requests.post(url, data=raw_data, headers=headers)
    #print(response.status_code)
    # 2. Verificar que la respuesta es correcta
    if response.status_code == 200:
        for cookie in response.cookies:
           if cookie.name == "MOCA-WS-SESSIONKEY":
               v_token =cookie.value
    
        url_item = url_wms_item +"?warehouseId="+warehouseId+"&itemNumber="+itemNumber
        cookies_item = {cookie.name:cookie.value}           
        response_item = requests.get(url_item,  cookies=cookies_item)
        if response_item.status_code == 200:     
           dataj = response_item.json()              
           o_description = dataj["items"][0]["description"]  

           return{ "url_token_wms"    : url_token_wms ,
                   "warehouseId"      : warehouseId,
                    "o_description"   : o_description
                  } 

if __name__ == "__main__":
   import uvicorn
   port= int(os.getenv("PORT",8000))
   uvicorn.run(app, host="0.0.0.0", port=port)