from fastapi import FastAPI

from .routes import planning

app = FastAPI()
app.include_router(planning.router)


@app.get("/")
def index():
    return {"status": "ok"}
