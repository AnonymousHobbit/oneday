import requests

def register_user(username, full_name, country, password):
    data = {
        "username": username,
        "full_name": full_name,
        "country": country,
        "password": password

    }

    requests.post("http://localhost:5000/users/register", data=data)
    print("[+] User registered")


def register_company(name, username, email, country, password):
    data = {
        "name": name,
        "username": username,
        "email": email,
        "country": country,
        "password": password
    }

    requests.post("http://localhost:5000/companies/register", data=data)
    print("[+] Company registered")

if __name__ == "__main__":
    register_user("test", "Test Tester", "Finland", "root")
    register_company("Red Bull", "redbull", "redbull@test.com", "Austria", "root")