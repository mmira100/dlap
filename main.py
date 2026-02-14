#main.py
from fastapi import FastAPI , Request
import requests
import json
import  os
from typing import Annotated

app = FastAPI()

with open("ejemplo1.txt", "w") as archivo:
    archivo.write("Este es un archivo de texto creado con Python.")

@app.get("/")

def root():
   return{ "url_token_wms" : "listo40"  }
                       
if __name__ == "__main__":
   import uvicorn
   port= int(os.getenv("PORT",8000))
   uvicorn.run(app, host="0.0.0.0", port=port)
