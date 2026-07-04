from fastapi import FastAPI
import uvicorn
from config import PORT
from api.routes import router

app = FastAPI(
    title="Video Processing Service",
    version="1.0.0"
)

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=PORT,
        reload=True,
    )