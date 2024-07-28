from fastapi import FastAPI
from .routes import router


app = FastAPI()

app.include_router(router, prefix="/comment", tags=["comments"])


@app.get("/")
def _health_check():
    return {"message": "Comment Service is running"}
