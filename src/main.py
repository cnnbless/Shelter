from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Shelter Platform API")

app.mount("/media", StaticFiles(directory="media"), name="media")

@app.get("/health")
async def health_check():
    return {"status": "ok"}