import logging
import sys


class Config:
    SECRET_KEY = 'STAND_UP_ALL_VICTIMS_OF_OPPRESSION'

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    logging.basicConfig(
        level=logging.NOTSET,
        filename='TestLogs.log',
        format='%(asctime)s\t%(levelname)s\t%(threadName)s\t%(name)s\t%(funcName)s:%(lineno)d\t%(message)s',
        datefmt='%Y%m%dT%H:%M:%S %Z'
    )
    TESTING = False  # Vitally important config value, if set to true the test suites will run frying the DB!
    ###
    DB_HOST = 'localhost'
    DB_PORT = 5432
    DB_NAME = 'postgres'
    DB_SCHEMA = 'katsuPROD'
    DB_USER = 'katsu'
    DB_PASSWORD = 'katsu'
    DB_MAX_CONNECTIONS = 50
    DB_MIN_CONNECTIONS = 5
    ###
    WTF_CSRF_ENABLED = True  # Helps prevent cross site request forgery. You always want this to be True.


class DevelopmentConfig(Config):
    logging.basicConfig(
        level=logging.NOTSET,
        filename='DevLogs.log',
        format='%(asctime)s\t%(levelname)s\t%(threadName)s\t%(name)s\t%(funcName)s:%(lineno)d\t%(message)s',
        datefmt='%Y%m%dT%H:%M:%S %Z'
    )
    TESTING = True
    ###
    DB_HOST = 'localhost'
    DB_PORT = 5432
    DB_NAME = 'postgres'
    DB_SCHEMA = 'katsuDEV'
    DB_USER = 'katsu'
    DB_PASSWORD = 'katsu'
    DB_MAX_CONNECTIONS = 50
    DB_MIN_CONNECTIONS = 5
    ###
    WTF_CSRF_ENABLED = False


class TestConfig(Config):
    logging.basicConfig(
        level=logging.DEBUG,
        filename='TestLogs.log',
        format='%(asctime)s\t%(levelname)s\t%(threadName)s\t%(name)s\t%(funcName)s:%(lineno)d\t%(message)s',
        datefmt='%Y%m%dT%H:%M:%S %Z',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    TESTING = True
    ###
    DB_HOST = 'localhost'
    DB_PORT = 5432
    DB_NAME = 'postgres'
    DB_SCHEMA = 'katsuTEST'
    DB_USER = 'katsu'
    DB_PASSWORD = 'katsu'
    DB_MAX_CONNECTIONS = 50
    DB_MIN_CONNECTIONS = 5
    ###
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
