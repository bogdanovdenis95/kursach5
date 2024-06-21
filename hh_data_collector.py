import requests
import psycopg2
from psycopg2 import Error


def get_employers(employer_ids):
    employers = []
    for employer_id in employer_ids:
        response = requests.get(f'https://api.hh.ru/employers/{employer_id}')
        if response.status_code == 200:
            employers.append(response.json())
        else:
            print(f"Failed to retrieve data for employer ID: {employer_id}")
    return employers


def get_vacancies(employer_id):
    vacancies = []
    page = 0
    while True:
        response = requests.get(f'https://api.hh.ru/vacancies?employer_id={employer_id}&page={page}')
        if response.status_code == 200:
            data = response.json()
            vacancies.extend(data['items'])
            if page >= data['pages'] - 1:
                break
            page += 1
        else:
            print(f"Failed to retrieve vacancies for employer ID: {employer_id}")
            break
    return vacancies


def insert_data(employers, vacancies):
    try:
        conn = psycopg2.connect(
            dbname='skypro',
            user='postgres',
            password='skypro',
            host='localhost',
            port='5433'
        )
        cur = conn.cursor()

        for employer in employers:
            cur.execute("""
                INSERT INTO employers (hh_id, name, description, url) 
                VALUES (%s, %s, %s, %s) 
                ON CONFLICT (hh_id) DO NOTHING 
                RETURNING id
            """, (employer['id'], employer['name'], employer.get('description', ''), employer['site_url']))
            row = cur.fetchone()
            if row is not None:
                employer_db_id = row[0]
            else:
                continue  # Skip if employer ID wasn't retrieved

            for vacancy in vacancies.get(employer['id'], []):
                salary = vacancy.get('salary')
                salary_from = salary.get('from') if salary else None
                salary_to = salary.get('to') if salary else None
                currency = salary.get('currency') if salary else None
                cur.execute("""
                    INSERT INTO vacancies (hh_id, employer_id, name, salary_from, salary_to, currency, published_at, url) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (hh_id) DO NOTHING
                """, (vacancy['id'], employer_db_id, vacancy['name'], salary_from, salary_to, currency, vacancy['published_at'], vacancy['alternate_url']))

        conn.commit()
        print("Data inserted successfully!")
    except psycopg2.Error as e:
        print(f"Error inserting data: {e}")
        conn.rollback()
    finally:
        if 'conn' in locals():
            cur.close()
            conn.close()


if __name__ == "__main__":
    employer_ids = ['1455', '78638','5713306', '2219347', '10347404', '8940297', '4599861', '5912899', '4219', '1740']  # Примеры ID компаний
    employers = get_employers(employer_ids)
    
    vacancies = {}
    for employer_id in employer_ids:
        vacancies[employer_id] = get_vacancies(employer_id)
    
    insert_data(employers, vacancies)
