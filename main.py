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

@app.get("/")
def root():
    return{"hello":url_token_wms }

if __name__ == "__main__":
   import uvicorn
   port= int(os.getenv("PORT",8000))
   uvicorn.run(app, host="0.0.0.0", port=port)