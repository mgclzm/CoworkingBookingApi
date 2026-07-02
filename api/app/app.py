from fastapi import FastAPI

from routes.user.router import user_router

def init_app() -> FastAPI:
    app = FastAPI(debug=True, 
                   title='Cowork Booking API (example)', 
                   description='Training project, aimed at practicing development metodologies and architectural patterns.')
    app.include_router(user_router)
    return app
