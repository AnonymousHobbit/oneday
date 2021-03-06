# Oneday
OneDay is a 'Bug Bounty' -platform where users can report vulnerabilities to companies involved.

You can test the application [here](https://onedaybb.herokuapp.com)
## Installation

### Prerequisites
* Python version 3.8 or up
* Postgresql database

### Configuration
Copy `src/.env.example` to `src/.env`.<br>
Set `DATABASE_URL` to PostgreSQL database connection string<br>
Set `SECRET_KEY` to application secret

### Running the program
Install all dependencies
```
$ pip3 install -r requirements.txt
```

Initialize the database
```
$ python3 build.py
```

Starting the application
```
$ flask run
```

To automatically create test data, run the following script after the application is running
```
$ python3 helper.py
```
## Features
* User can easily report a new vulnerability to company
* Companies can close or accept the reports
* Companies can easily add or remove urls in the scope. 
* Users and companies can send new messages to the report to make their communication easy.
* Company must have atleast one scope added before user can report a vulnerability
