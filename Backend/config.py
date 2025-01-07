#!/usr/bin/env python3

"""
    The configuration file for the flask app
    """


from dotenv import load_dotenv
from os import getenv
import subprocess
from datetime import timedelta


load_dotenv()  # Load environment variables from .env file


class Config():
    """
        The base configuration class """

    MYSQL_USERNAME = getenv("MYSQL_USERNAME")
    MYSQL_PASSWORD = getenv("MYSQL_PASSWORD")
    MYSQL_DB = getenv("MYSQL_DB")
    MYSQL_HOST = getenv("MYSQL_HOST")

    print("MYSQL_USERNAME: ", MYSQL_USERNAME)
    print("MYSQL_PASSWORD: ", MYSQL_PASSWORD)
    print("MYSQL_DB: ", MYSQL_DB)
    print("MYSQL_HOST: ", MYSQL_HOST)

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}/{}".format(
            MYSQL_USERNAME,
            MYSQL_PASSWORD,
            MYSQL_HOST,
            MYSQL_DB)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SECRET_KEY = getenv("SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
