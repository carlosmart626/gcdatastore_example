# Google Data Store example

This a very simple API to create, read, update, delete **(CRUD)** of a bike store handling only the product list.

This example works uses [Google Data Store](https://cloud.google.com/datastore/docs/concepts/overview)
as storage option for a Django project.

## Run local project
This project uses Docker for develop and production

- create `dev.env`
    ```
    DEBUG=[ True or False ]
    DATA_BACKEND=datastore
    SECRET_KEY=[ your secret key ]
    PROJECT_ID=[ your project id ]
    GOOGLE_APPLICATION_CREDENTIALS=[ credentials json path ]
    ```
- run `docker-compose up`
- open browser at `http://localhost:8000`

## Run production using nginx and gunicorn project
This project uses Docker for develop and production

- create `secrets` folder and paste your google json credentials
- create `dev.env`
    ```
    DEBUG=[ False ]
    DATA_BACKEND=datastore
    SECRET_KEY=[ your secret key ]
    PROJECT_ID=[ your project id ]
    GOOGLE_APPLICATION_CREDENTIALS=[ credentials json path ]
    ```
- run `docker-compose -f production.yml up -d`
- open browser at `http://[ your ip]`

## Run tests locally
- create a virtualenv `python3 -m venv bike_store`
- activate virtualenv `pip install -r bike_store/requirements.txt`
- export `dev.env` file as environment variables
- run test using `python manage.py tests`
