from fastapi import FastAPI
from post_routes import post_router
from get_routes import get_router

app = FastAPI(title="Ferme connectée", version="1.0")

app.include_router(post_router, prefix="/api/v1")
app.include_router(get_router, prefix="/api/v1")

@app.get("/ping")
def ping():
    return {"message": "backend is alive"}
