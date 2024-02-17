import requests
from dotenv import load_dotenv

from config import HH_URL, EMPLOYERS_ID_LIST

load_dotenv()


class HeadHunterAPI:
    """Класс для получения данных с hh.ru через API"""
    def __init__(self) -> None:
        self.params = {
            "employer_id": EMPLOYERS_ID_LIST,
            "per_page": 100
        }

    def get_data(self, page=0) -> list[dict]:
        self.params["page"] = page
        return requests.get(url=HH_URL, params=self.params).json()["items"]
