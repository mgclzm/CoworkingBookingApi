from fastapi import FastAPI
import punq

def init_app() -> FastAPI:
    return FastAPI(debug=True, 
                   title='Cowork Booking API (example)', 
                   description='Training project, aimed at practicing development metodologies and architectural patterns.')

def init_container() -> punq.Container:
    container = punq.Container()

    return container