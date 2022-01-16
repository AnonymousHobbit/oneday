import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
from os import getenv

load_dotenv()

try:
    connection = psycopg2.connect(getenv("DATABASE_URL"))
    connection.autocommit = True
    cursor = connection.cursor()

    print("[+] Removing all tables")
    cursor.execute("DROP TABLE IF EXISTS scope CASCADE")
    cursor.execute("DROP TABLE IF EXISTS reports CASCADE")
    cursor.execute("DROP TABLE IF EXISTS companies CASCADE")
    cursor.execute("DROP TABLE IF EXISTS users CASCADE")
    
    print("[+] Creating all tables")
    cursor.execute(open("schema.sql", "r").read())

except (Exception, Error) as error:
    print("[!] Error while connecting to PostgreSQL", error)

finally:
    if (connection):
        cursor.close()
        connection.close()
        print("[+] PostgreSQL connection is closed")
