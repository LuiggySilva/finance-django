## *.env* to DEV
- **DEBUG** = `True` or `False` 
- **SECRET_KEY** = `String`
- **DJANGO_ALLOWED_HOSTS** = `String list`


## *.env* to PROD
- **DEBUG** = `True` or `False` 
- **SECRET_KEY** = `String`
- **DJANGO_ALLOWED_HOSTS** = `String list`
- **SQL_ENGINE** = `django.db.backends.postgresql`
- **SQL_DATABASE** = `String`
- **SQL_USER** = `String`
- **SQL_PASSWORD** = `String`
- **SQL_HOST** = `db`
- **SQL_PORT** = `5432`
- **DATABASE** = `postgres`


## *.env.db* to DEV
- ***POSTGRES_USER** = `String equals to .env SQL_USER`
- ***POSTGRES_PASSWORD** = `String equals to .env SQL_PASSWORD`
- ***POSTGRES_DB** = `String to DataBase name`  


## *.env.prod.db* to PROD
- ***POSTGRES_USER** = `String equals to .env.prod SQL_USER`
- ***POSTGRES_PASSWORD** = `String equals to .env.prod SQL_PASSWORD`
- ***POSTGRES_DB** = `String to DataBase name`  

> **POSTGRES_DB** in `.env.db`' and `.env.prod.db` files must have different names

## Run project without Docker
- `python ./app/manage.py runserver`
- Go to [http://localhost:8000](http://localhost:8000) in browser


## Run project with Docker in DEV
- `docker-compose up -d --build`
- Go to [http://localhost:8000](http://localhost:8000) in browser


## Run project with Docker in PROD
- `docker-compose -f docker-compose.prod.yml up -d --build`
- Go to [http://localhost:1337](http://localhost:1337) in browser


## Stop and Remove all project Docker files
1. `docker container stop finance-django-web-1`
2. `docker container stop finance-django-db-1`
3. `docker rm finance-django-web-1`
4. `docker rm finance-django-db-1`
5. `docker rmi finance-django-web`
6. `docker volume remove finance-django_postgres_data`
7. `docker network remove finance-django_default`
