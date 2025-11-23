from fastapi import FastAPI

from app.endpoints import router

app = FastAPI(title="Riot Take-Home Test")

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "API is running"}