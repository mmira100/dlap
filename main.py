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
        # 4. Cookies se pasa el Token MOCA
        cookies_item = {cookie.name:cookie.value}           
        response_item = requests.get(url_item,  cookies=cookies_item)
        # 5. Verificar que la respuesta es correcta de WMS BY Item
        if response_item.status_code == 200:     
           dataj = response_item.json()              
           o_description = dataj["items"][0]["description"]  
           o_resourceId  = dataj["items"][0]["resourceId"]
           o_displayUom  = dataj["items"][0]["displayUom"]

           return{ "items": {
                    "itemNumber"       : itemNumber,
                    "warehouseId"     : warehouseId,
                    "description"     : o_description,
                    "displayUom"      : o_displayUom
                     }
                   }  
                       
if __name__ == "__main__":
   import uvicorn
   port= int(os.getenv("PORT",8000))
   uvicorn.run(app, host="0.0.0.0", port=port)
