from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.apis import router
from app.db import connect_db, disconnect_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await connect_db(app)
    yield
    # shutdown
    await disconnect_db(app)
    
app = FastAPI(lifespan=lifespan)

app.include_router(router)
