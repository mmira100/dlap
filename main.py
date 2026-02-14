#main.py
from fastapi import FastAPI , Request
import requests
import json
import  os
from typing import Annotated

app = FastAPI()

with open("ejemplo1.txt", "w") as archivo:
    archivo.write("Este es un archivo de texto creado con Python.")

#Abrir el archivo de configuración para urls y credenciales
from pathlib import Path
ruta_base = Path(__file__).parent 
archivo_ruta = ruta_base / "config.json"
with open(archivo_ruta, 'r') as f:
    data = json.load(f) # Lee y convierte a diccionario en un solo paso
    url_token_wms = data["items"][0]["url_token_wms"]
    usr_id_wms    = data["items"][0]["usr_id_wms"]
    password_wms  = data["items"][0]["password_wms"]
    url_wms_item  = data["items"][0]["url_wms_item"]

# La API publica de WMS BY que queremos consumir para el token 
url = url_token_wms
# Las credenciales se pasan por RAW 
raw_data = f'{{"usr_id": "{usr_id_wms}", "password": "{password_wms}"}}'
headers = {"Content-Type": "application/json"}

@app.get("/items")

def root(warehouseId: str, itemNumber: str, request: Request):
    # 1. Consumir la API externa usando requests
    response = requests.post(url, data=raw_data, headers=headers)    
    # 2. Verificar que la respuesta es correcta del token
    if response.status_code == 200:
        for cookie in response.cookies:
           if cookie.name == "MOCA-WS-SESSIONKEY": 
               v_token =cookie.value
        # 3. Armar la url de WMS BY para la info de items
        url_item = url_wms_item +"?warehouseId="+warehouseId+"&itemNumber="+itemNumber
        return{ "url_token_wms1"  : url_token_wms,
                 "v_token1"       : v_token,
                 "url_wms_by_item": url_item }
                       
if __name__ == "__main__":
   import uvicorn
   port= int(os.getenv("PORT",8000))
   uvicorn.run(app, host="0.0.0.0", port=port)
