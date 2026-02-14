#main.py
from fastapi import FastAPI
import  os

app= FastAPI()

@app.get("/")
def root():
    return{"hello":"world"}

if __name__ == "__main__":
   import uvicorn
   port= int(os.getenv("PORT",8000))
   uvicorn.run(app, host="0.0.0.0", port=port)