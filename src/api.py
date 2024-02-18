import requests
from dotenv import load_dotenv

from config import HH_URL_EMPLOYERS

load_dotenv()


class HeadHunterAPI:
    """Класс для получения данных с hh.ru через API"""

    @staticmethod
    def get_data() -> list[dict]:
        employers_list = []

        for employer in HH_URL_EMPLOYERS:
            employer_data = requests.get(url=employer).json()
            employer_dict = {'id': employer_data['id'],
                             'name': employer_data['name'],
                             'alternate_url': employer_data['alternate_url'],
                             'vacancies_url': requests.get(url=employer_data['vacancies_url']).json()
                             }
            employers_list.append(employer_dict)
        return employers_list
