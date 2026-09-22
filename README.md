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

## Setup instructions
create a target folder and move into it

run:
git clone https://github.com/SlainV/NewsStream.git

move into newsstream folder
run:
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser

After creating the superuser:

1. Run the server: python manage.py runserver
2. Log into Django Admin. (http://localhost:8000/admin/)
3. Add the superuser to the Administrator group.
4. Thereafter manage users via the NewsStream Administrator Dashboard (http://localhost:8000/accounts/admin-dashboard/)