import psycopg2

class DBManager:
    def __init__(self, dbname, user, password, host, port):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
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

# Пример использования
if __name__ == "__main__":
    db = DBManager(dbname='skypro', user='postgres', password='skypro', host='localhost', port='5433')
    
    print("Companies and vacancies count:")
    print(db.get_companies_and_vacancies_count())

    print("\nAll vacancies:")
    print(db.get_all_vacancies())

    print("\nAverage salary:")
    print(db.get_avg_salary())

    print("\nVacancies with higher salary:")
    print(db.get_vacancies_with_higher_salary())

    print("\nVacancies with keyword 'Python':")
    print(db.get_vacancies_with_keyword('Python'))

    db.close()
