from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from app.config import PORT
from app.api.routes import router

from app.utils.supervisor_manager import SupervisorManager

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


if __name__ == "__main__":

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=PORT,
        reload=True,
    )