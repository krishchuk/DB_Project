from src.api import HeadHunterAPI
from src.database import DBManager


def main():
    hh = HeadHunterAPI()
    hh_data = hh.get_data()
    db = DBManager('hh_db')
    db.create_database('hh_db')
    db.create_table('hh_db')
    db.save_data_to_database(hh_data, 'hh_db')


if __name__ == '__main__':
    main()
