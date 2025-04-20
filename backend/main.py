from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from routes import estimate, cities

origins = [
    "http://localhost:5173",
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(">>> Starting the app")
    from model import model

    yield
    # any cleanup here
    print(">>> Stopping the app")


app = FastAPI(title="House Price Estimator", version="0.1.0", lifespan=lifespan)
app.include_router(estimate.router)
app.include_router(cities.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn

    # Check if the WYCENAPPKA_PROD environment variable is set to true
    is_prod = os.environ.get("WYCENAPPKA_PROD", "").lower() == "true"

    # Set production mode settings if needed
    if is_prod:
        print("Running in production mode")
        uvicorn.run(app="main:app", host="0.0.0.0", port=8001, log_level="info")
    else:
        print("Running in development mode")
        uvicorn.run(app="main:app", host="localhost", port=8001, reload=True)
