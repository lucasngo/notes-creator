This app runs on flask application.
To run the app, you first need to download every packages from requirement.txt 
After downloading packages, run flask using command on terminal.

For mac os, 
export FLASK_APP=application.py
flask run

For windows,
set FLASK_APP=application.py
flask run

*** note : this application needs to use local machine database. you need to replace the string inside engine=create_engine('postgresql+psycopg2://postgres:Duclong123@localhost:5432/notes') with the url to your database ***

