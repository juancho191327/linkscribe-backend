from load_model import model_load
from fastapi import FastAPI
from scrapper_controller import router as scrapper_router
from fastapi import Depends, Request
from scrapper import Scrapper

app = FastAPI()

async def get_model(request:Request):
    return request.app.state.model

async def get_traductor(request:Request):
    return request.app.state.traductor

async def get_scrapper(request:Request):
    return request.app.state.scrapper

@app.on_event("startup")
def load_model():
    print("Cargando Modelo...")
   
    model = model_load()
    print("Modelo Cargado!!!")
    app.state.model = model
    
@app.on_event("startup")    
def load_scrapper():
    scrapper=Scrapper()
    app.state.scrapper= scrapper
    
@app.on_event("shutdown")
def shutdown_event():
    print("Apagando aplicativo Adios...")
  
app.include_router(
    scrapper_router, 
    tags=["scrapper"],
    prefix="/scrapper"
)

@app.get("/hi")
def hi():
    return {"message": "Hola Mundo. ATT:API"}

