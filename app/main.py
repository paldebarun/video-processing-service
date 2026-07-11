from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.routes import router

from utils.supervisor_manager import SupervisorManager

supervisor = SupervisorManager()


@asynccontextmanager
async def lifespan(app: FastAPI):

    try:

        supervisor.generate_config()

        supervisor.start()

        yield

    finally:

        supervisor.stop()


app = FastAPI(
    title="Video Processing Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)