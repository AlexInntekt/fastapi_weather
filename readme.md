## Run locally with pipenv

echo 'export ENV=local' > .env

Make sure you set the neccesary variables in .env file. You can find them in the settings/local.py
The default settings module that is used is settings.local and it already has default values for all the variables. 
The connection to AWS S3 and Dynamodb is made via the AWS CLI profile. Configure one using 'aws configure'

pipenv shell

pipenv install

fastapi dev main.py

curl 127.0.0.1:8000/weather?city=Kronstadt

# Using cache

In order to use S3 as a cache tool for the files, you need to configure an AWS boto3 client via `aws configure`
Check AWS documentation for this.
Also, you need to set USE_S3_CACHE = True in the settings module.

## Run locally with Docker

sudo docker compose build

sudo docker-compose up


## Deploy proposal:

You can use run a docker image instance for a development environment.
For production you can scale the application with docker swarm.


## Auto-generated docs
127.0.0.1:8000/docs



