from fastapi import FastAPI

from routes import estimate

app = FastAPI(title="House Price Estimator", version="0.1.0")
app.include_router(estimate.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
