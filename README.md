# Проект HeadHunter Data Collector

Этот проект предназначен для сбора данных с API HeadHunter (hh.ru) о работодателях и вакансиях, их сохранения в базу данных PostgreSQL и предоставления возможности работы с этими данными.

## Как начать использовать проект

1. **Настройка окружения**:
   - Установите Python версии 3.x: [скачать Python](https://www.python.org/downloads/)
   - Установите PostgreSQL: [скачать PostgreSQL](https://www.postgresql.org/download/)
   - Создайте базу данных под названием `skypro`.
   - Запустите PostgreSQL и убедитесь, что сервер базы данных запущен.

2. **Установка и настройка проекта**:
   - Клонируйте репозиторий: `git clone https://github.com/ваш_проект`
   - Перейдите в каталог проекта: `cd ваш_проект`
   - Установите необходимые зависимости:
     ```bash
     pip install -r requirements.txt
     pip install psycopg2
     ```

3. **Создание таблиц в базе данных**:
   - Запустите скрипт `db_settings.py` для создания необходимых таблиц в базе данных PostgreSQL.
   - Внесите необходимые изменения в параметры подключения (`dbname`, `user`, `password`, `host`, `port`) в соответствии с вашими настройками PostgreSQL.

4. **Сбор и вставка данных**:
   - Запустите скрипт `hh_data_collector.py` для получения данных о работодателях и вакансиях с API HeadHunter.
   - Убедитесь, что база данных PostgreSQL (`skypro`) доступна и работает.

5. **Операции с базой данных**:
   - Используйте `db_manager.py` для выполнения запросов к базе данных.
   - При необходимости измените параметры подключения (`dbname`, `user`, `password`, `host`, `port`).

## Функциональность

- **Сбор данных**: Скрипт `hh_data_collector.py` собирает данные о работодателях и вакансиях с API HeadHunter и сохраняет их в базу данных.
- **Управление базой данных**: `db_manager.py` предоставляет методы для выполнения запросов к базе данных, таких как получение списка вакансий с высокой зарплатой или поиск по ключевому слову.

## Примеры использования

```python
# Пример использования db_manager.py
from db_manager import DBManager

db = DBManager(dbname='skypro', user='postgres', password='skypro', host='localhost', port='5433')

print("Количество компаний и вакансий:")
print(db.get_companies_and_vacancies_count())

print("\nВсе вакансии:")
print(db.get_all_vacancies())

print("\nСредняя зарплата:")
print(db.get_avg_salary())

print("\nВакансии с высокой зарплатой:")
print(db.get_vacancies_with_higher_salary())

print("\nВакансии с ключевым словом 'Python':")
print(db.get_vacancies_with_keyword('Python'))

db.close()
