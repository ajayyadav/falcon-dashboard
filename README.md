falcon-web
==========

This is a web interface for the Apache Falcon Project. For local development, if you are aware of virtualenv and virtualenvwrapper then it's highly recommended to create a new virtualenv and skip step 3. 


Getting Started
================

1. Clone the project 
             git clone git@github.com:ajayyadav/falcon-web.git

2. cd to project's diretory
      1. <code>cd falcon-web </code>

3. Install pip ( you have to use sudo if you are not using virtualenvs )
      1. download get-pip.py from https://bootstrap.pypa.io/get-pip.py
      2. <code>sudo python get-pip.py </code>

Debugging Tip: If you get an error like Permission Denied: then you probably forgot to use sudo

4. Install requirements: <code>sudo pip install -r requirements.txt </code>

5. Start the server: 
      1. <code>cd falcon </code>
      2. <code>python manage.py runserver</code>

6. You can view following urls as of now
      1. http://localhost:8000/dashboard/
      2. http://localhost:8000/dashboard/process/create/

