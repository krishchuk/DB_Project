from src.api import HeadHunterAPI
from src.database import DBManager


def main():
    hh = HeadHunterAPI()
    hh_data = hh.get_data()
    db = DBManager('hh_db')
    db.create_database('hh_db')
    db.create_table()
    db.save_data_to_database(hh_data)

    while True:
        print('\nВыберите действие:')
        print('1. Получить список компаний и количество их вакансий.')
        print('2. Получить список всех вакансий.')
        print('3. Получить среднюю зарплату по вакансиям.')
        print('4. Получить список вакансий с зарплатой выше средней.')
        print('5. Найти вакансии по ключевому слову.')
        print('6. Выход.')

        user_input = input('\nВведите соответсвующее запросу число: ')

        if user_input == '1':
            companies_and_vacancies_count = db.get_companies_and_vacancies_count()
            print('\nСписок компаний и вакансий:')
            for company, count in companies_and_vacancies_count:
                print(company, '-', count, 'вакансий')

        elif user_input == '2':
            all_vacancies = db.get_all_vacancies()
            print('\nСписок всех вакансий:')
            for vacancy_id, vacancy_name, salary_from, salary_to, title, url, employer_id in all_vacancies:
                if salary_from == 0 and salary_to == 0:
                    print(f'{vacancy_name} (зарплата не указана): {url}')
                elif salary_from == 0 and salary_to != 0:
                    print(f'{vacancy_name} до {salary_to} руб.: {url}')
                elif salary_from != 0 and salary_to == 0:
                    print(f'{vacancy_name} от {salary_from} руб.: {url}')
                elif salary_from != 0 and salary_to != 0:
                    print(f'{vacancy_name} от {salary_from} до {salary_to} руб.: {url}')

        elif user_input == '3':
            avg_salary = db.get_avg_salary()
            print(f'\nСредняя зарплата по всем вакансиям: {'%.2f' % avg_salary} руб.')

        elif user_input == '4':
            vacancies_with_higher_salary = db.get_vacancies_with_higher_salary()
            print(f'\nВакансии с зарплатой выше средней ({'%.2f' % db.get_avg_salary()} руб.):')
            for company, url in vacancies_with_higher_salary:
                print(company, '-', url)

        elif user_input == '5':
            keyword = input('\nВведите ключевое слово: ')
            vacancies_with_keyword = db.get_vacancies_with_keyword(keyword)
            print('\nВакансии по ключевому слову:')
            for vacancy, url in vacancies_with_keyword:
                print(vacancy, '-', url)

        elif user_input == '6':
            break


if __name__ == '__main__':
    main()
