#!/usr/bin/env python3
"""
    Flask app for the backend RESTFull API
    """

import os
import subprocess

lock_file = ".setup_done"

# Check if the setup has already been done
def setup_user_and_database():
    if os.path.exists(lock_file):
        print("The setup for Mysql user and databse has already been done.")
        return

    print("Setting up the MySQL user and database.")
    try:
        result = subprocess.run(["../SetUp/setup_user_and_database.sh"], check=True)
        print("Bash script executed successfully.")
        with open(lock_file, "w") as f:
            f.write("The setup has been done.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the Bash script: {e}")


from flask import Flask
from models.base import db
from config import Config
from flask_migrate import Migrate

from models.user import User
from models.plan import Plan
from models.custom_exercise import CustomExercise
from models.record import Record
from models.exercise import Exercise
from models.day import Day
from models.workout_session import WorkoutSession


app = Flask(__name__)

# Get the configuration from config.py
app.config.from_object(Config)

# initialize and connect the app to sqlalchemy
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    setup_user_and_database()
    db.create_all()

# Register the blueprints
from api.v1.views import views_bp
app.register_blueprint(views_bp)

if __name__ == '__main__':
    app.run(host="localhost", port="5001",debug=True)
