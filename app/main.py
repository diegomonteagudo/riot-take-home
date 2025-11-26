from fastapi import FastAPI

from app.endpoints import router

app = FastAPI(
    title="Riot Take-Home Test",
    description="An API to encrypt, decrypt, sign and verify JSON payloads.",
    contact={
        "name": "Diego Monteagudo",
        "url": "https://github.com/diegomonteagudo/riot-take-home"}
)

app.include_router(router)

@app.get("/")
async def root() -> dict:
    return {"message": "API is running"}