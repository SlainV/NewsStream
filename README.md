# NewsStream

A Django-based news publishing platform

## Table of Contents

[Features](#features)

[Roles and abilities](#roles)

[Installation prerequisites](#installation-prerequisites)

[Setup Instructions](#setup-instructions)

[System quickstart](#using-the-system)

[API](#article-api)

## Features

- Custom user model
- Role-based access control
- Publishers and affiliations
- Article management
- Editorial review workflow
- Newsletter subscriptions
- REST API
- Role specific dashboard (depends on logged in user role)

## Roles

Users can register as a Reader, Journalist, or Editor. The selected role is stored on the custom User model and synchronized with the matching Django Group.

Administrators can update a user's primary role through the application's Administrator Dashboard.

- Administrator
  - Assigns additional roles to other users
- Publisher Manager
  - Manages Publishers (create, disable Publications, assign Editors and Journalists)
- Journalist
  - Submit, edit and delete articles, create, edit and delete own newsletters.
- Editor
  - Reviews submitted articles, edit and delete articles, edit and delete newsletters.
- Reader
  - Read articles and subscribe to newsletters

## Installation prerequisites

- python 3 with pip

- git

- MariaDB

```
NAME: 'newsstream_db',      # Your database name

USER: 'newsstream_user',    # Your database user (root if no SQL user is created)

PASSWORD: 'strongpassword', # Your user password (root password if no dedicated user)
```

-- username and password can be changed in config/settings.py, make sure to adapt it to match your installation settings.

### Configure MariaDB

After installation of Maria DB, open a terminal and log into a session.

- If MariaDB was not added to the system PATH you may have to run these commands from the /bin/ folder in the MariaDB installation location.

```
mysql -u root -p
```

You will be prompted to enter your root password (which was created during MariaDB installation, not related to newsStream)

Create the Database - run:

```
CREATE DATABASE newsstream_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

The database is now ready to receive the command to create the relevant tables.

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

- Add the superuser to the Administrator group (Click Users, select Admin, scroll to Groups and move the Administrator role over to the Chosen Groups column.

- Thereafter manage user role change via the NewsStream Administrator Dashboard  if required (http://localhost:8000/accounts/admin-dashboard/). 

## Using the system

### Creating users

Assuming you've completed the installation (on port 8000) and created an Administrator:

- Register (by using http://localhost:8000/accounts/register/)
  
  - a user who will become a Reader.
  
  - a user which will become an Editor.
  
  - a user who will become a Journalist.
  
  - a user who will become a Publisher Manager

- After registration user roles an be changed by the Admin user on the Admin Dashboard (http://localhost:8000/accounts/admin-dashboard/)

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

- A Reader can subscribe to either a Publisher or Journalist.

- Logged in as Reader, click 'Newsletter Subscription' from the top navigation.

- On the next page all eligible Publications and Journalists are listed, and can be subscribed to by clicking 'Subscribe'.

## Article API

Token-authenticated article endpoints include:

- Approved article listing

- Subscribed article listing

- Single article retrieval

- Journalist article creation

- Journalist and Editor article updates

- Journalist and Editor article deletion

Journalists may create articles using affiliated publishers and may update or delete only their own articles. Editors may update or delete any article. Readers have view-only access.

Articles created through the API are saved as drafts and must still pass through the existing Editor review and approval workflow.
