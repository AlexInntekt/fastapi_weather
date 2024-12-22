
## Run locally with pipenv (Method 1)



Setup: 

The app runs with a set of application variables that you can change. You cand find them in the settings module settings/local.py
You can overite them there or better in the .env file

In the settings/local.py, you can also find default values. 

This setup expects you to have an AWS S3 bucket and a DynamoDB table configured on your AWS profile.
The connection to AWS S3 and Dynamodb is made via the AWS CLI profile. Configure one using 'aws configure'

Create an .env file where you will store the environment variables that will be injected in the settings and 
will overwrite the default ones:
`echo 'export ENV=local' > .env`

Create a virtual environment:

`pipenv shell`

Install the dependencies from Pipfile:

`pipenv install` 

Run the application locally:
`fastapi dev main.py`

Test the API endpoint with curl in your shell: (works on Linux and Macos)
`curl 127.0.0.1:8000/weather?city=Kronstadt`




## Run locally with Docker (Method 2)

`sudo docker compose build`

`sudo docker-compose up`


# Using cache

In order to use S3 as a cache tool for the files, you need to configure an AWS client via `aws configure`
Check AWS documentation for this.
Also, you need to set USE_S3_CACHE = True in the settings module.

Similarly, the application expects you to have a dynamodb table configured on your AWS profile.
You can change its name in settings.


## Deploy proposal:

You can use run a docker image instance for a development environment.
For production you can scale the application with docker swarm on several nodes.


## Auto-generated docs
127.0.0.1:8000/docs



