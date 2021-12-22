import logging
import subprocess
import sys

from fastapi import FastAPI

from app.routers import subscriptions, courses, subscribers

# Perform db upgrade
subprocess.run(
    [
        "alembic",
        "upgrade",
        "head"
    ],
    stdout=subprocess.DEVNULL,
)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

app = FastAPI()
app.include_router(subscriptions.router)
app.include_router(courses.router)
app.include_router(subscribers.router)


@app.get("/")
def read_root():
    return "subscriptions api"
