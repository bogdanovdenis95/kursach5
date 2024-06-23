# HH Data Collector

Этот проект собирает данные о вакансиях с сайта hh.ru и сохраняет их в базу данных PostgreSQL. Также он предоставляет различные методы для работы с собранными данными.

## Структура проекта

- `config_example.py`: Пример конфигурационного файла с параметрами подключения к базе данных.
- `db_settings.py`: Модуль для настройки базы данных (создание таблиц).
- `db_manager.py`: Модуль для работы с базой данных (запросы к таблицам).
- `hh_data_collector.py`: Модуль для получения данных с сайта hh.ru и их вставки в базу данных.
- `main.py`: Точка входа в приложение, которая связывает все модули вместе.
- `requirements.txt`: Файл с зависимостями проекта.

## Установка

1. Клонируйте репозиторий:
    ```sh
    git clone https://github.com/bogdanovdenis95/kursach5.git
    cd kursach5
    ```

2. Создайте и активируйте виртуальное окружение:
    ```sh
    python -m venv venv
    source venv/bin/activate  # Для Windows: venv\Scripts\activate
    ```

3. Установите зависимости:
    ```sh
    pip install -r requirements.txt
    ```

4. Создайте файл `config.py`, скопировав `config_example.py`:
    ```sh
    cp config_example.py config.py
    ```

5. Откройте `config.py` и заполните его параметрами подключения к базе данных:
    ```python
    DB_NAME = 'your_database_name'
    DB_USER = 'your_database_user'
    DB_PASSWORD = 'your_database_password'
    DB_HOST = 'your_database_host'
    DB_PORT = 'your_database_port'
    ```

## Использование

1. Запустите главный скрипт:
    ```sh
    python main.py
    ```

2. Скрипт выполнит следующие шаги:
    - Создаст таблицы в базе данных.
    - Соберет данные о работодателях и вакансиях с сайта hh.ru.
    - Вставит собранные данные в базу данных.
    - Выполнит несколько запросов к базе данных и выведет результаты.

## Структура базы данных

Проект создает две таблицы: `employers` и `vacancies`.

### Таблица `employers`
- `id`: SERIAL PRIMARY KEY
- `hh_id`: INT NOT NULL UNIQUE
- `name`: VARCHAR(255) NOT NULL
- `description`: TEXT
- `url`: VARCHAR(255)

### Таблица `vacancies`
- `id`: SERIAL PRIMARY KEY
- `hh_id`: INT NOT NULL UNIQUE
- `employer_id`: INT REFERENCES employers(id)
- `name`: VARCHAR(255) NOT NULL
- `salary_from`: INT
- `salary_to`: INT
- `currency`: VARCHAR(10)
- `published_at`: TIMESTAMP
- `url`: VARCHAR(255)

## Лицензия

Этот проект лицензирован на условиях лицензии MIT. Подробнее см. файл [LICENSE](LICENSE).
