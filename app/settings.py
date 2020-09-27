import configparser as Configparser

conf = Configparser.RawConfigParser()
conf_path = r'config.txt'
conf.read(conf_path)

HOST = conf.get("ud", "HOST")
DATABASE_HOST = conf.get("ud", "DATABASE_HOST")
DATABASE_NAME = conf.get("ud", "DATABASE_NAME")

TOKEN = conf.get("ud", "TOKEN")
