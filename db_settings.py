import psycopg2

class DBSetup:
    def __init__(self, dbname, user, password, host, port):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
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

if __name__ == "__main__":
    db_setup = DBSetup(dbname='skypro', user='postgres', password='skypro', host='localhost', port='5433')
    db_setup.create_tables()
    db_setup.close()
