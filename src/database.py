from typing import Any

import psycopg2

from config import config

params = config()


class DBManager:
    """Класс для работы с БД"""

    def __init__(self, database_name):
        self.params = params

    @classmethod
    def create_database(cls, database_name):
        """Создает БД"""
        try:
            conn = psycopg2.connect(**params)
            with conn.cursor() as curr:
                conn.autocommit = True
                curr.execute(f'CREATE DATABASE {database_name}')
            conn.close()
        except Exception as error:
            print('Error creating database', error)

    @staticmethod
    def create_table(database_name):
        """Создает таблицы employers и employers в указанной БД"""
        conn = None
        try:
            conn = psycopg2.connect(**params, dbname=database_name)
            with conn.cursor() as curr:
                curr.execute('DROP TABLE IF EXISTS employers CASCADE;')
                curr.execute('DROP TABLE IF EXISTS vacancies CASCADE;')
                curr.execute(
                    'CREATE TABLE employers('
                    'employer_id int PRIMARY KEY,'
                    'company_name varchar(255),'
                    'url text);')
                print('Таблица employers создана успешно')
                curr.execute(
                    'CREATE TABLE vacancies('
                    'vacancy_id int PRIMARY KEY,'
                    'vacancy_name varchar(255),'
                    'salary_from int,'
                    'salary_to int,'
                    'title text,'
                    'url text,'
                    'employer_id int REFERENCES employers(employer_id));')
                print('Таблица vacancies создана успешно')
                conn.commit()
        except Exception as error:
            print('Error creating tables', error)
        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def get_companies_and_vacancies_count():
        """Получает список всех компаний и количество вакансий у каждой компании"""
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as curr:
                curr.execute('SELECT company_name, COUNT(*) as vacancy_count FROM employers GROUP BY company_name')
                answer = curr.fetchall()
        return answer

    @staticmethod
    def get_all_vacancies():
        """Получает список всех вакансий"""
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as curr:
                curr.execute('SELECT * FROM vacancies')
                answer = curr.fetchall()
        return answer

    @staticmethod
    def get_avg_salary():
        """Получает среднюю зарплату по вакансиям"""
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as curr:
                curr.execute('SELECT salary_from, salary_to FROM vacancies')
                answer = curr.fetchall()
                for row in answer:
                    if row[0] != 0 and row[1] != 0:
                        avg_salary = (row[1] + row[0]) / 2
                    elif row[0] != 0 and row[1] == 0:
                        avg_salary = row[0]
                    elif row[0] == 0 and row[1] != 0:
                        avg_salary = row[1]
                    elif row[0] == 0 and row[1] == 0:
                        avg_salary = 0
        return avg_salary

    @staticmethod
    def get_vacancies_with_higher_salary():
        """Получает список вакансий с зарплатой выше средней по всем вакансиям"""
        avg_salary = DBManager.get_avg_salary()
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as curr:
                curr.execute('SELECT vacancy_name, url FROM vacancies WHERE (salary_from + salary_to) / 2 > %s',
                             (avg_salary,))
                answer = curr.fetchall()
        return answer

    @staticmethod
    def get_vacancies_with_keyword(keyword):
        """Получает список всех вакансий, в названии которогых есть переданные ключевые слова"""
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as curr:
                curr.execute('SELECT vacancy_name, url FROM vacancies WHERE vacancy_name LIKE %s',
                             ('%' + keyword + '%',))
                answer = curr.fetchall()
        return answer

    @staticmethod
    def save_data_to_database(data: list[dict[str, Any]], database_name: str):
        """Сохранение данных о каналах и видео в базу данных."""
        conn = psycopg2.connect(dbname=database_name, **params)
        with conn.cursor() as curr:
            for employer in data:
                curr.execute(
                    """
                    INSERT INTO employers (employer_id, company_name, url)
                    VALUES (%s, %s, %s)
                    RETURNING employer_id
                    """,
                    (employer['id'], employer['name'], employer['alternate_url'])
                )
                for vacancy in employer['vacancies_url']['items']:
                    if vacancy['salary'] is None:
                        vacancy['salary'] = {}
                    elif vacancy['salary']['from'] is None:
                        vacancy['salary']['from'] = 0
                    elif vacancy['salary']['to'] is None:
                        vacancy['salary']['to'] = 0
                    curr.execute(
                        """
                        INSERT INTO vacancies (vacancy_id, vacancy_name, salary_from, salary_to, title, url, employer_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        (vacancy['id'], vacancy['name'], vacancy['salary'].get('from', 0), vacancy['salary'].get('to', 0),
                         vacancy['snippet']['responsibility'], vacancy['alternate_url'], vacancy['employer']['id'])
                    )
        conn.commit()
        conn.close()
