from fastapi import FastAPI

def init_app() -> FastAPI:
    return FastAPI(debug=True, 
                   title='Cowork Booking API (example)', 
                   description='Training project, aimed at practicing development metodologies and architectural patterns.')
