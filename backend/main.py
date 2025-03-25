from fastapi import FastAPI
from contextlib import asynccontextmanager

from routes import estimate, cities


@asynccontextmanager
async def lifespan(app: FastAPI):
    # any preprocessing here
    print(">>> Starting the app")
    yield
    # any cleanup here
    print(">>> Stopping the app")


app = FastAPI(title="House Price Estimator", version="0.1.0", lifespan=lifespan)
app.include_router(estimate.router)
app.include_router(cities.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", host="localhost", port=8001, reload=True)
