from fastapi import FastAPI

from app.routers import auth, tasks

app = FastAPI()

app.include_router(auth.router)
app.include_router(tasks.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
