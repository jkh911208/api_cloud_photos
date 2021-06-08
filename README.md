## Cloud Photos REST API Service

This is backend part of Cloud Photos App.
This will handle all database CRUD operation and save the media to local storage.

## If you made database schema change

You will need to run 
```
alembic revision --autogenerate 
```
in order to update the database schema. You will need to stop the docker-compose and restart the docker-compose will automatically update the DB

## Start backend service

1. Install docker-compose in your dev machine
2. run
```
docker-compose build && docker-compose up
```

you will have postgres Database and python backend service running, that include create all the database schema automatically

3. navigate to http://localhost:5000/docs in your favorite browser to access swagger UI

## Running service in production mode
It will add frontend verifycation on every request and swagger UI will be disabled.

In docker-compose.yml file change PRODUCTION=0 to PRODUCTION=1

In actual production I use seperate dockerfile to build the container image to run the service with gunicorn, not using docker-compose.

Checkout deploy.Dockerfile to see actual production container build process.