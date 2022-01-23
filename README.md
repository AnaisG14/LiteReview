# LiteReview
Application to request and publish book reviews.
Each user can follow other users or have followers.
Application developed with the django framework.

## A- Cloned the GitHub project 
### 1- Create a folder and place yourself inside it.
    whith linux :
    $ mkdir <mon_dossier>
    $ cd <mon_dossier>
### 2- Clone the GitHub folder "LiteReview"
    $ git clone https://github.com/AnaisG14/LiteReview.git
### 2- Create and active a virtual environment (with linux):
#### -> Create the virtual environment
    Place yourself in the cloned folder
    $ cd LiteReview
    $ python3 -m venv <environnement name>

    exemple: 
    $ python3 -m venv envLite
#### -> Active your virtual environment
    $ source <environnement_name>/bin/activate

    exemple : 
    $ source envLite/bin/activate
### 3- Install the required packets :
    $ pip install -r requirements.txt

## B- Manage the db with sqlite3
### 1- Initialize the sqlite db
    $ python manage.py flush
### 2- Create a super User
    $ python manage.py createsuperuser
    And enter a name and a password (the email address is optional)
### 3- Manage the db on a browser
    http://127.0.0.1:8000/admin/

## C- Launch the application
### 1- Launch the local server with the terminal :
    $ python3 manage.py runserver
### 2- Open the site with your local server on a browser :
    http://127.0.0.1:8000/

