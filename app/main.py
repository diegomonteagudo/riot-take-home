from fastapi import FastAPI

app = FastAPI(title="Riot Take-Home Test")

@app.get("/")
async def root():
    return {"message": "API is running"}