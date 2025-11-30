# Titanic Cleaner Service 
## Install
cd DataCleaner
source .venv/bin/activate

## Run in local
(.venv) poetry run python api.py

## Test and generate coverage report
(.venv) poetry run coverage report -m


## Build and Run in docker container
docker build -t data-clean:latest .
docker run -p 8000:8000 --name data-clean-1 -it data-clean:latest
