from configparser import ConfigParser

EMPLOYERS_ID_LIST = [
    "2180",
    "15478",
    "1740",
    "1429999",
    "2748",
    "2501",
    "84585",
    "3529",
    "2136954",
    "64174"
]

HH_URL_EMPLOYERS = [f"https://api.hh.ru/employers/{employer}" for employer in EMPLOYERS_ID_LIST]


def config(filename="config.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db
