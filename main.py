from db_settings import DBSetup
from db_manager import DBManager
from hh_data_collector import get_employers, get_vacancies, insert_data

def main():
    # Step 1: Setup database
    db_setup = DBSetup()
    db_setup.create_tables()
    db_setup.close()

    # Step 2: Collect data from HH API
    employer_ids = ['1455', '78638', '5713306', '2219347', '10347404', '8940297', '4599861', '5912899', '4219', '1740']
    employers = get_employers(employer_ids)

    vacancies = {}
    for employer_id in employer_ids:
        vacancies[employer_id] = get_vacancies(employer_id)

    # Step 3: Insert data into database
    insert_data(employers, vacancies)

    # Step 4: Perform some database queries
    db = DBManager()
    
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

if __name__ == "__main__":
    main()
