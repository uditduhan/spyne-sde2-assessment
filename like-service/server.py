from fastapi import FastAPI
from .routes import router

app = FastAPI()

app.include_router(router, prefix="/like", tags=["likes"])


@app.get("/")
def _health_check():
    return {"message": "Like Service is running"}
