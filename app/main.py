from fastapi import FastAPI

from app.database import Base, engine
from app.routers import auth, workflows, instances

app = FastAPI(title="Workflow Engine API", version="0.1.0")

app.include_router(auth.router)
app.include_router(workflows.router)
app.include_router(instances.router)


@app.on_event("startup")
def on_startup():
    # Minimal setup: create tables if they don't exist.
    # Swap this for Alembic migrations once the schema stabilizes.
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check():
    return {"status": "ok"}
