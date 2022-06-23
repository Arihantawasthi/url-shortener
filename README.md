# url-shortener
Shortens the provided url

## Requirements:
Make sure python and postgresql is installed in the machine

## Setting up the Postgresql Database:
 ```
 sudo su - postgres
 psql
 CREATE DATABASE url_shortener;
 CREATE USER <username> WITH PASSWORD '<password>';
 ALTER ROLE <username> SET client_encoding TO 'utf8';
 ALTER ROLE <username> SET default_transaction_isolation TO 'read committed';
 ALTER ROLE <username> SET timezone TO 'UTC';
 GRANT ALL PRIVILEGES ON DATABASE url_shortener TO <username>;
 \q
 exit
 ```
 
 ## Setting up the application:
 
 ` git clone git@github.com:Arihantawasthi/url-shortener.git `
 ` cd url-shortener `
 
 Create Virtual Environment (Optional):
 ` virtualenv venv `
 
 To activate virtual environment:
 ` source ./venv/bin/activate `
 
 ## Installing the Requirements
 ` pip install -r requirements.txt `
 
 ## Setting up Environment Variables
 ```
 export FLASK_APP=application
 export FLASK_DEBUG=1
 export DATABASE_URL=postgresql://<username>:<password>@localhost:5432/url_shortener
 ```
 
 ## Running the application
 ` flask run `
