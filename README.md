# Project Setup

Clone repository using command below
```
git clone https://github.com/masterr314/PP_lab_repo.git
```


Install [pyenv](https://github.com/pyenv/pyenv) on your machine.

Then Install Python 3.8.10 using pyenv.
```
pyenv install 3.8.10
```

Create your project directory and set there local python version.
```
pyenv local 3.8.10
```

.python-version file should be created in your project directory.

After this install [pipenv](https://pipenv.pypa.io/en/latest/) for creating virtualenv and dependencies management.
```
pip install pipenv
```

Create virtualenv using **pipenv** and install all dependencies.
```
pipenv install --python 3.8.10
```

After this start **WSGI** server using [Waitress](https://flask.palletsprojects.com/en/2.2.x/deploying/waitress/)
```
waitress-serve --host 127.0.0.1 application:app
```

## Start app using 'flask'

Set **FLASK_APP** on Windows
```
set FLASK_APP=application
```

Set **FLASK_APP** on UNIX
```
export FLASK_APP=application
```

Run app
```
flask run
```

Create db
```
flask create_db
```

Drop db
```
flask drop_db
```