from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api_gate.pg import router as pg_router
import datetime as dt


app = FastAPI()

routers = [pg_router]
for router in routers:
    app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    t = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = "FastAPI is a modern, fast (high-performance), web framework for building APIs with Python based on standard Python type hints."
    return [{"Message": msg, "DateTime": t}]


@app.get("/test")
async def read_tst():
    t = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return [{"Message": "Test Page", "DateTime": t}]
