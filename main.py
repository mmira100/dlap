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
    
    return{ "url_token_wms" :url_token_wms ,
            "warehouseId"   :warehouseId } 

if __name__ == "__main__":
   import uvicorn
   port= int(os.getenv("PORT",8000))
   uvicorn.run(app, host="0.0.0.0", port=port)