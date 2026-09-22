# NewsStream

A Django-based news publishing platform

## Features
- Custom user model
- Role-based access control
- Publishers and affiliations
- Article management
- Editorial review workflow
- Newsletter subscriptions
- REST API
- Administrator dashboard

## Roles
- Administrator
- Publisher Manager
- Journalist
- Editor
- Reader

## Installation prerequisites
python 3 with pip
git
MariaDB
'NAME': 'newsstream_db',         # Your database name
'USER': 'newsstream_user',       # Your database user
'PASSWORD': 'strongpassword',    # Your user password
 -- username and password can be changed in config/settings.py

## Setup instructions
Move to the folder where you want to run the app from.

run:
git clone https://github.com/SlainV/NewsStream.git

move into NewsStream folder
run:
python -m venv venv
.venv/bin/activate.bat (assuming Windows OS)

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser

python manage.py create_groups

After creating the superuser:

1. Run the server: python manage.py runserver
2. Log into Django Admin. (http://localhost:8000/admin/)
3. Add the superuser to the Administrator group.
4. Thereafter manage users via the NewsStream Administrator Dashboard (http://localhost:8000/accounts/admin-dashboard/)
