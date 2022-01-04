# Oneday
Bug bounty platform where user can report vulnerabilities to companies

## Installation

### Configuration
Copy `src/.env.example` to `src/.env`.
Set `DATABASE_URL` to PostgreSQL database connection string
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

## ToDo
- [x] Login & register
- [ ] Profile page
- [ ] Create an organisation
- [ ] Organisation home page
- [ ] Display reports in profile.
- [ ] Submit a report