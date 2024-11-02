from fastapi import FastAPI
from app.api.v1.endpoints import items

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}

app.include_router(items.router, prefix="/v1/items", tags=["items"])
