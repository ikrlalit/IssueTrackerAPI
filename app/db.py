import asyncpg
from fastapi import FastAPI

DATABASE_URL = "postgresql://postgres:root@localhost:5432/issuetrackerdb"

async def connect_db(app: FastAPI):
    app.state.pool = await asyncpg.create_pool(
        DATABASE_URL,
        min_size=5,
        max_size=20
    )

async def disconnect_db(app: FastAPI):
    await app.state.pool.close()
