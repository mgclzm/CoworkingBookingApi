from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.app.container import init_container, typed_resolve
from api.routes.booking.router import booking_router
from api.routes.user.router import user_router
from api.routes.workspace.router import workspace_router
from infra.task_broker.base import BaseTaskBroker


@asynccontextmanager
async def lifespan(app: FastAPI):
    container = init_container()
    broker = typed_resolve(container, BaseTaskBroker)
    await broker.startup()
    yield
    await broker.shutdown()


def init_app() -> FastAPI:
    app = FastAPI(
        debug=True,
        title="Coworking Booking API (example)",
        description="Training project, aimed at practicing development methodologies and architectural patterns.",
        lifespan=lifespan,
    )
    app.include_router(user_router)
    app.include_router(workspace_router)
    app.include_router(booking_router)
    return app
