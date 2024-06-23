import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        self.cur.execute("""
            SELECT e.name, COUNT(v.id) 
            FROM employers e
            JOIN vacancies v ON e.id = v.employer_id
            GROUP BY e.name
        """)
        return self.cur.fetchall()

    def get_all_vacancies(self):
        self.cur.execute("""
            SELECT e.name, v.name, v.salary_from, v.salary_to, v.currency, v.url 
            FROM vacancies v
            JOIN employers e ON e.id = v.employer_id
        """)
        return self.cur.fetchall()

    def get_avg_salary(self):
        self.cur.execute("""
            SELECT AVG((v.salary_from + v.salary_to) / 2.0)
            FROM vacancies v
            WHERE v.salary_from IS NOT NULL AND v.salary_to IS NOT NULL
        """)
        return self.cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        self.cur.execute("""
            SELECT e.name, v.name, v.salary_from, v.salary_to, v.currency, v.url 
            FROM vacancies v
            JOIN employers e ON e.id = v.employer_id
            WHERE ((v.salary_from + v.salary_to) / 2.0) > %s
        """, (avg_salary,))
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        self.cur.execute("""
            SELECT e.name, v.name, v.salary_from, v.salary_to, v.currency, v.url 
            FROM vacancies v
            JOIN employers e ON e.id = v.employer_id
            WHERE v.name ILIKE %s
        """, (f'%{keyword}%',))
        return self.cur.fetchall()

    def close(self):
        self.cur.close()
        self.conn.close()
