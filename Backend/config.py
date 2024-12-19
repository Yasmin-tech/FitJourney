#!/usr/bin/env python3

"""
    The configuration file for the flask app
    """


from dotenv import load_dotenv
from os import getenv


load_dotenv()  # Load environment variables from .env file


class Config():
    """
        The base configuration class """

    # Set default values for environment variables if they are not provided

    MYSQL_USERNAME = getenv("MYSQL_USERNAME", "fit_journey_user")
    MYSQL_PASSWORD = getenv("MYSQL_PASSWORD", "my_passowrd")
    MYSQL_DB = getenv("MYSQL_DB", "FitJourney")
    MYSQL_HOST = getenv("MYSQL_HOST", "localhost")

    SQLALCHEMY_DATABASE_URI = "mysql+mysqlclient://{}:{}@{}/{}".format(
            MYSQL_USERNAME,
            MYSQL_PASSWORD,
            MYSQL_HOST,
            MYSQL_DB)
