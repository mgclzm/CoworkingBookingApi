from fastapi import FastAPI

from api.routes.booking.router import booking_router
from api.routes.user.router import user_router
from api.routes.workspace.router import workspace_router


def init_app() -> FastAPI:
    app = FastAPI(
        debug=True,
        title="Coworking Booking API (example)",
        description="Training project, aimed at practicing development methodologies and architectural patterns.",
    )
    app.include_router(user_router)
    app.include_router(workspace_router)
    app.include_router(booking_router)
    return app
