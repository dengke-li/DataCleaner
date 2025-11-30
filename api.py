from fastapi import FastAPI

from app.models import PassengerRaw, PassengerClean
from app.cleaning.pipeline import titanic_cleaner
from error_handlers import register_exception_handlers

app = FastAPI(title="Titanic passager data Cleaner", version="1.0")
# Register error handlers
register_exception_handlers(app)

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

