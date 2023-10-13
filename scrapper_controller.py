from pydantic import BaseModel
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from load_model import model_load
from scrapper import Scrapper
from fastapi import Request, Depends
import typing
import numpy as np
from typing import List

class URLItem(BaseModel):
    link: str

router = InferringRouter()

async def get_model(request:Request):
    return request.app.state.model

async def get_traductor(request:Request):
    return request.app.state.traductor

async def get_scrapper(request:Request):
    return request.app.state.scrapper

@cbv(router)

class scrapper_controller:
    
    model: model_load = Depends(get_model)
    scrapper: Scrapper =Depends(get_scrapper)
    
    @router.post("/predict")
    
    def predict(self,URLS:List[URLItem]):
        URLS = URLS[0].link
        print(URLS)
        article=self.scrapper.read_url(URLS)
        chunks=self.scrapper.text_processor(article)
        resume=self.scrapper.summarize(chunks)
        prediction=self.model.predict([resume])
        title=self.scrapper.obtener_titulo(URLS)
        title=str(title[0])
        img=self.scrapper.obtener_imagen(URLS)
        return prediction,resume,title,img
    
    
    





