import configparser as Configparser

conf = Configparser.RawConfigParser()
conf_path = r'config.txt'
conf.read(conf_path)

DATABASE_HOST = conf.get("ud", "DATABASE_HOST")
DATABASE_NAME = conf.get("ud", "DATABASE_NAME")

API_KEY = conf.get("ud", "API_KEY")
API_KEY_SECRET = conf.get("ud", "API_KEY_SECRET")
