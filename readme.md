## Run locally with pipenv

echo 'export ENV=local' > .env

pipenv shell

pipenv install

fastapi dev main.py

curl 127.0.0.1:8000/weather?city=Kronstadt

## Run locally with Docker

sudo docker compose build

sudo docker-compose up


## Auto-generated docs
127.0.0.1:8000/docs



