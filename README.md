# Data Cleaner Service 
## Description
Data Cleaner Service is a web application built with FastAPI that provides endpoints 
for cleaning and preprocessing datasets.

## Run in local
(.venv) poetry run python api.py

## Test and generate coverage report
(.venv) poetry run coverage report -m


## Build and Run in docker container
docker build -t data-clean:latest .

docker run -p 8000:8000 --name data-clean-1 -it data-clean:latest
