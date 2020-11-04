from dotenv import load_dotenv
import pymysql
import os


class DBHelper:
    def __init__(self):
        load_dotenv(verbose=True)
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASSWD = os.getenv("DB_PASSWD")

    def conn(self, database="crimemap"):
        return pymysql.connect(
            host="localhost", db=database, user=self.DB_USER, passwd=self.DB_PASSWD, charset="UTF8"
        )

    def get_all_inputs(self):
        conn = self.conn()
        try:
            query = "SELECT description FROM crimes"
            with conn.cursor() as cursor:
                cursor.execute(query)
            return cursor.fetchall()
        finally:
            conn.close()

    def add_input(self, data):
        conn = self.conn()
        try:
            query = "INSERT INTO crimes (description) VALUES ('{}');".format(data)
            with conn.cursor() as cursor:
                cursor.execute(query)
                conn.commit()
        finally:
            conn.close()

    def clear_all(self):
        conn = self.conn()
        try:
            query = "DELETE FROM crimes;"
            with conn.cursor() as cursor:
                cursor.execute(query)
                conn.commit()
        finally:
            conn.close()
