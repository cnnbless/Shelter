from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.api.shelters import router as shelters_router
from src.api.animals import router as animals_router

app = FastAPI(title="Shelter Platform API")

app.mount("/media", StaticFiles(directory="media"), name="media")

app.include_router(shelters_router)
app.include_router(animals_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}