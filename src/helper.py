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
        print("[+] User registered")


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
        print("[+] Company registered")


if __name__ == "__main__":
    register_user("admin", "Test Tester", "Finland", "admin")
    register_company("Red Bull", "redbull", "redbull@test.com", "Austria", "root")
    register_company("Kivinen", "kivi", "kivinen@test.com", "Finland", "root")