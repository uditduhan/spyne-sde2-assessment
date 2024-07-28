from fastapi import FastAPI
from .models import Base
from .routes import router

app = FastAPI()

app.include_router(router, prefix="/discussion", tags=["discussion"])


@app.get("/")
def _health_check():
    return {"message": "Discussion Service is running"}
