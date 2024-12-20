## Run locally with pipenv

echo 'export ENV=local' > .env

pipenv shell

pipenv install

fast dev main.py

curl 127.0.0.1:8000/weather?city=Kronstadt

## Run locally with Docker

sudo docker compose build

sudo docker-compose up


## Auto-generated docs
127.0.0.1:8000/docs



[//]: # (## Maintanance)

[//]: # (From time to time, sync the requirements file with pipfile:)

[//]: # ()
[//]: # (pipenv lock -r > requirements.txt)