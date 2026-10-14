from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import FRONTEND_DIST
from app.database import connect, create_schema
from app.routes import bookings, hosts, reports
from app.seed import seed_if_empty


@asynccontextmanager
async def lifespan(application: FastAPI):
    connection = connect()
    create_schema(connection)
    seed_if_empty(connection)
    connection.close()
    yield


app = FastAPI(title="Renter Trust Network", lifespan=lifespan)

for module in (hosts, bookings, reports):
    app.include_router(module.router)

# Serves the built React app. Mounted last so the /api routes take priority.
if FRONTEND_DIST.is_dir():
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")
