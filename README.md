**Hello everyone, this project is not completed and I am working on it.**
# HOW MAKE THIS WORK ON YOUR DEVICE?:
## Get and initialize the project:
1. First of all get this project by bellow commands:
```
mkdir project && cd project
git init
git pull https://github.com/amirhossein226/Simple-pdf-parser-with-easygui.git
```

2. Create a virtual environment and activate it:
```
python3 -m venv .venv
source .venv/bin/activate
```

3. Install requirements of project from requirements.txt:
```
pip install -r requirements.txt
```

## Set the environment variables:
4. Create a file named **.env** on project's root directory and copy contents of **sample.env** file on this file:
```
cat sample.env > .env
```

5. Create a secret Key using below command for your project and make a copy from your generated secret key and place it in front of **DJANGO_SECRET** on .env file.
```
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

6. Define your allowed hosts on **DJANGO_ALLOWED_HOSTS**
7. Configure your database settings.I am working with postgres and if you like it too then use below steps to config it for this project:
    - Make sure that **docker** is installed on your system.If it isn't, make search __How install docker on my windows/linus/mac__
    - Get the **postgres:16.2** image from docker using `docker pull postgres:16.2`
    - Run the a docker container for this image using bellow command:
    `docker run --rm --name postgres-db -e POSTGRES_DB=db_test -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -p 5432:5432 -v my-project-data:/var/lib/postgresql/data/ -d postgres:16.2`
    > At this point you must have postgres running on the background, you can be sure about it by running `docker ps` and see if the container by **postgres-db** is running or not.
    - Open **.env** file again and make below changes on it:
        - `DJANGO_DB_ENGINE=django.db.backends.postgresql`
        - `DJANGO_DB_NAME=db_test`
        - `DJANGO_DB_USER=user` 
        - `DJANGO_DB_PASSWORD=password`
        - `DJANGO_DB_HOST=localhost`
        - `DJANGO_DB_PORT=5432`
        - The DJANGO_DB_NAME,DJANGO_DB_USER and DJANGO_DB_PASSWORD are the value that you set when running the docker container(POSTGRES_DB, POSTGRES_USER and POSTGRES_PASSWORD respectively).
8. Set the configuration related to email. For example you could use your own google account. For this purpose use [this tutorial](https://dev.to/krishnaa192/creating-google-app-password-for-django-project-4oj3).
9. On **login** page, I implemented the google authentication and if you want to make this implementation work, execute a project on [google developer console](https://console.developers.google.com/project) for yourself and use the Client id and Client secret which you will get at the end and set the GOOGLE_OAUTH2_CLIENT_ID and GOOGLE_OAUTH2_CLIENT_SECRET environment variables on **.env** file.

10. If you want to run this project on you local computer using **HTTPS** protocol, then you must do some aditional steps too. Use [This tutorial](https://forum.djangoproject.com/t/https-during-development/10509)






