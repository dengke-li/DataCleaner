from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from app.models import PassengerRaw, PassengerClean
from app.cleaning.pipeline import titanic_cleaner


app = FastAPI(title="Titanic passager data Cleaner", version="1.0")


@app.post("/clean/passenger", response_model=PassengerClean)
def clean_passager(payload: PassengerRaw):
    try:
        cleaned = titanic_cleaner.run(payload)
    except Exception as e:
       raise e
    return cleaned

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

