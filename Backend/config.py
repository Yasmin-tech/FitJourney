#!/usr/bin/env python3

"""
    The configuration file for the flask app
    """


from os import getenv
import subprocess
from datetime import timedelta
from flask_swagger_ui import get_swaggerui_blueprint


class Config:
    """
    The base configuration class"""

    MYSQL_USERNAME = getenv("MYSQL_USERNAME")
    MYSQL_PASSWORD = getenv("MYSQL_PASSWORD")
    MYSQL_DB = getenv("MYSQL_DB")
    MYSQL_HOST = getenv("MYSQL_HOST")

    print("MYSQL_USERNAME: ", MYSQL_USERNAME)
    print("MYSQL_PASSWORD: ", MYSQL_PASSWORD)
    print("MYSQL_DB: ", MYSQL_DB)
    print("MYSQL_HOST: ", MYSQL_HOST)

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}/{}".format(
        MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # engine = create_engine(SQLALCHEMY_DATABASE_URI)
    # session_factory = sessionmaker(bind=engine)
    # Session = scoped_session(session_factory)

    # JWT configuration
    SECRET_KEY = getenv("SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # Swagger configuration
    SWAGGER_URL = "/api/docs"
    API_URL = "/static/swagger.yaml"  # Path to your Swagger YAML file
    SWAGGER_CONFIG = {"app_name": "FitJourney API"}
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL, API_URL, config=SWAGGER_CONFIG
    )
