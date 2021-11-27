from fastapi import FastAPI

from app.routers import subscriptions, courses

app = FastAPI()
app.include_router(subscriptions.router)
app.include_router(courses.router)


@app.get("/")
def read_root():
    return "subscriptions api"
