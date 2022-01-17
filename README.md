# Oneday
OneDay is a 'Bug Bounty' -platform where users can report vulnerabilities to companies involved.


## Installation

### Configuration
Copy `src/.env.example` to `src/.env`.<br>
Set `DATABASE_URL` to PostgreSQL database connection string<br>
Set `SECRET_KEY` to application secret

### Running the program
Install all dependencies
```
$ pip install -r requirements.txt
```

Initialize the database
```
$ python src/build.py
```

Starting the application
```
$ python src/app.py
```

To automatically create test data, run the following script after the application is running
```
$ python src/helper.py
```
## Features
* User can easily report a new vulnerability to company
* Companies can close or accept the reports
* Companies can easily add or remove urls in the scope. 
* Users and companies can send new messages to the report to make their communication easy.
* Company must have atleast one scope added before user can report a vulnerability
