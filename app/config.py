import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False


class DevelopConfig(Config):
    DEBUG = True


config_by_name = dict(dev=DevelopConfig)