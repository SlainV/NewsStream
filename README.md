# NewsStream

A Django-based news publishing platform

## Table of Contents

[Features](#features)

[Roles and abilities](#roles)

[Installation prerequisites](#installation-prerequisites)

[Setup Instructions](#setup-instructions)

[System quickstart](#using-the-system)

##

## Features

- Custom user model
- Role-based access control
- Publishers and affiliations
- Article management
- Editorial review workflow
- Newsletter subscriptions
- REST API
- Administrator dashboard for assigning roles to users
- Role specific dashboard (depends on logged in user role)

##

## Roles

Like with many real-world systems (LMS, Institutional Repositories) new users register for the lowest possible access (Reader), and higher permissions have to be granted afterwards

- Administrator
  - Assigns and removes roles of other users
- Publisher Manager
  - Manages Publishers (create, disable Publications, assign Editors and Journalists)
- Journalist
  - Submits articles
- Editor
  - Reviews submitted articles
- Reader
  - Read articles and subscribe to newsletters

##

## Installation prerequisites

- python 3 with pip
  
- git
  
- MariaDB
  

```
NAME: 'newsstream_db',      # Your database name

USER: 'newsstream_user',    # Your database user

PASSWORD: 'strongpassword', # Your user password
```

-- username and password can be changed in config/settings.py

##

## Setup instructions

Move to the folder where you want to run the app from.

- Clone the repository from GitHub by running:
  

```cmd
git clone https://github.com/SlainV/NewsStream.git
```

- Create the Python Virtual Environment and activate it with:
  

```cmd
cd newsstream
python -m venv venv
source venv/bin/activate.bat
```

Install the required Python libraries with:

```cmd
pip install -r requirements.txt
```

Create database tables, relevant user groups and the superuser with:

```cmd
python manage.py migrate

python manage.py createsuperuser

python manage.py create_groups
```

After completing the commands run the server:

```cmd
python manage.py runserver
```

- Log into Django Admin. (http://localhost:8000/admin/)
  

- Add the superuser to the Administrator group (Users, select Admin, scroll to Groups and move the Administrator role over t the Chosen Groups column.
- Thereafter manage users via the NewsStream Administrator Dashboard (http://localhost:8000/accounts/admin-dashboard/). Using the Admin Dashboard was a design decision which will not change.

##

## Using the system

### Creating users

Assuming you've completed the installation (on port 8000) and created an Administrator:

- Register (by using http://localhost:8000/accounts/register/)
  
  - a user who will become a Publication Manager.
    
  - a user which will become an Editor.
    
  - a user who will become a Journalist.
    
- After registration assign the roles to the users using the Admin user on the Admin Dashboard (http://localhost:8000/accounts/admin-dashboard/)
  

### Creating a publication (Publication Manager)

- Now, logging in as the Publication Manager, create a Publisher using the 'Publisher Dashboard' link on their Dashboard.
  
- Assign an Editor and Journalist to the Publisher on the Manage Staff link for the Publisher on the Publication Manager Dashboard.
  

### Creating an article (Journalist)

- Logging in with the Journalist account, go to the Journalist Area (from their Dashboard) and click on Create Article to create a new article.
  
- Add the content, and Save as Draft.
  

### Approving an article (Editor)

- Logging in as the Editor, find the 'Editor Area' on their Dashboard, and click 'Review queue.'
  
- On the next page, click 'Review' and Accept or Reject the article with an optional comment.
  

### Reading the articles

- Any role (and anonymous) can read articles, but you need to be logged in to subscribe to a Publisher or Journalist.

### Newsletter subscription

- You can subscribe to either a Publisher or Journalist.
  
- With any logged in role, click 'Newsletter Subscription' from the top navigation.
  
- On the next page all eligible Publications and Journalists are listed, and can be subscribed to by clicking 'Subscribe'.