import requests
from bs4 import BeautifulSoup

def register_user(username, full_name, country, password):
    data = {
        "username": username,
        "full_name": full_name,
        "country": country,
        "password": password

    }

    r = requests.post("http://localhost:5000/users/register", data=data)
    soup = BeautifulSoup(r.text, "html.parser")
    
    if error := soup.find("p", {"class": "errortext"}):
        print(f"[-] {error.text}")
    else:
        print(f"[+] User '{username}' registered, log in with: {username}:{password}")


def register_company(name, username, email, country, password):

    data = {
        "name": name,
        "username": username,
        "email": email,
        "country": country,
        "password": password
    }

    r = requests.post("http://localhost:5000/companies/register", data=data)
    soup = BeautifulSoup(r.text, "html.parser")
    if error := soup.find("p", {"class": "errortext"}):
        print(f"[-] {error.text}")
    else:
        print(f"[+] Company '{username}' registered, log in with: {username}:{password}")

if __name__ == "__main__":
    #Create users
    register_user("admin", "Test Tester", "Finland", "admin")
    register_user("user", "Test User", "Finland", "user")

    #Create companies
    register_company("Test", "test", "test@test.com", "Austria", "root")
    register_company("Kivinen", "kivi", "kivinen@test.com", "Finland", "root")
