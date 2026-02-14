#main.py
from fastapi import FastAPI , Request
import requests
import json
import  os
from typing import Annotated
app= FastAPI()




@app.get("/")

def obtener_datos_externos():
                   return{ 
                        "items": {
                        "url_token_wms"    : "listo" 
                        }
                       } 

if __name__ == "__main__":
   import uvicorn
   port= int(os.getenv("PORT",8000))
   uvicorn.run(app, host="0.0.0.0", port=port)