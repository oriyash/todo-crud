from fastapi import FastAPI

from .routers.api_router import router as api_router

app: FastAPI = FastAPI()

app.include_router(api_router)
