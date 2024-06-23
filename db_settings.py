import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

class DBSetup:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        self.cur = self.conn.cursor()

    def create_tables(self):
        commands = (
            """
            CREATE TABLE IF NOT EXISTS employers (
                id SERIAL PRIMARY KEY,
                hh_id INT NOT NULL UNIQUE,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                url VARCHAR(255)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS vacancies (
                id SERIAL PRIMARY KEY,
                hh_id INT NOT NULL UNIQUE,
                employer_id INT REFERENCES employers(id),
                name VARCHAR(255) NOT NULL,
                salary_from INT,
                salary_to INT,
                currency VARCHAR(10),
                published_at TIMESTAMP,
                url VARCHAR(255)
            )
            """
        )
        try:
            for command in commands:
                self.cur.execute(command)
            self.conn.commit()
            print("Tables created successfully!")
        except psycopg2.Error as e:
            print(f"Error creating tables: {e}")
            self.conn.rollback()

    def close(self):
        self.cur.close()
        self.conn.close()
