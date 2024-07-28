from fastapi import FastAPI
from .routes import router

app = FastAPI()

app.include_router(router, prefix="/user", tags=["users"])


@app.get("/")
def _health_check():
    return {"message": "User Service is running"}
