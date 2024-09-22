from fastapi import FastAPI
from app.api.casts import casts
from app.api.db import metadata, database, engine

# Créer toutes les tables définies dans le métadonnées
metadata.create_all(engine)

# Initialiser l'application FastAPI
app = FastAPI(openapi_url="/api/v1/casts/openapi.json", docs_url="/api/v1/casts/docs")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Inclure le routeur pour les casts
app.include_router(casts, prefix='/api/v1/casts', tags=['casts'])
