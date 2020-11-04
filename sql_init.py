from dotenv import load_dotenv
import pymysql
import os

load_dotenv(verbose=True)
DB_USER = os.getenv("DB_USER")
DB_PASSWD = os.getenv("DB_PASSWD")

conn = pymysql.connect(host="localhost", user=DB_USER, passwd=DB_PASSWD, charset="UTF8")

try:
    with conn.cursor() as cursor:
        sql = "CREATE DATABASE IF NOT EXISTS crimemap"
        cursor.execute(sql)
        sql = """CREATE TABLE IF NOT EXISTS crimemap.crimes (
            id int NOT NULL AUTO_INCREMENT,
            latitude FLOAT(10,6),
            longitude FLOAT(10,6),
            date DATETIME,
            category VARCHAR(50),
            description VARCHAR(1000),
            updated_at TIMESTAMP,
            PRIMARY KEY (id)
        )"""
        cursor.execute(sql)
        conn.commit()
finally:
    conn.close()
