from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# Initialize the Prometheus Instrumentator
instrumentator = Instrumentator()

# Instrument the FastAPI app
instrumentator.instrument(app).expose(app)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/health")
def health_check():
    # comment out the following line to simulate a failing health check
    raise HTTPException(status_code=500, detail="Internal Server Error")
    return {"status": "ok"}
