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
from api.v1.views import views_bp
from flask_jwt_extended import JWTManager
from auth import auth_bp
from errors import errors_bp

from models.user import User
from models.role import Role
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


# Aautomatically create the Admin role when the Flask app starts
def setup_admin_role():

    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")

    # Debugging statements to check environment variables
    print(f"ADMIN_EMAIL: {admin_email}")
    print(f"ADMIN_PASSWORD: {admin_password}")
    
    if not admin_email or not admin_password:
        print("Environment variables for Admin email and/or password are not set.")
        raise SystemExit("Error: Environment variables for Admin email and/or password are not set.")

    admin_role = Role.find_role_by_name("Admin")
    admin_user = User.find_user_by_email(admin_email)
    if not admin_role or not admin_user:

        if not admin_role:
            admin_role = Role(name="Admin")
            db.session.add(admin_role)
            db.session.commit()
            print("Admin role created successfully.")

        if not admin_user:
            admin_user = User(
                first_name="Admin",
                last_name="Admin",
                email=os.getenv("ADMIN_EMAIL"),
                password=os.getenv("ADMIN_PASSWORD")
            )
        admin_user.roles.append(admin_role)
        db.session.add(admin_user)
        db.session.commit()
        print("Admin role is assigned to the Admin user.")
    else:
        print("Admin role already exists.")

with app.app_context():
    setup_user_and_database()
    db.create_all()
    setup_admin_role()

# initialize the app to use JWT
jwt = JWTManager(app)
jwt.init_app(app)

# Register the blueprints
app.register_blueprint(views_bp)
app.register_blueprint(errors_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(app.config['SWAGGERUI_BLUEPRINT'])


if __name__ == '__main__':
    app.run(host="localhost", port="5000",debug=True)
