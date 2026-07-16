from fastapi import FastAPI

from api.routes.user.router import user_router

def init_app() -> FastAPI:
    app = FastAPI(debug=True, 
                   title='Coworking Booking API (example)', 
                   description='Training project, aimed at practicing development methodologies and architectural patterns.')
    app.include_router(user_router)
    return app
