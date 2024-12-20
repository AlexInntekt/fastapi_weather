## Run locally with pipenv

echo 'export ENV=local' > .env

# Make sure you set all the neccesary variables in .env file. You can find them in the settings/local.py

pipenv shell

pipenv install

fastapi dev main.py

curl 127.0.0.1:8000/weather?city=Kronstadt

# Using cache

In order to use S3 as a cache tool for the files, you need to configure an AWS boto3 client via `aws configure`
Check AWS documentation for this.

## Run locally with Docker

sudo docker compose build

sudo docker-compose up


## Auto-generated docs
127.0.0.1:8000/docs



