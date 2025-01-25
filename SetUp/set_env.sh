#!/bin/bash

# Set up the default environment variables
echo "Setting up environment variables..."

# Set your MySQL username that will have access and all privileges to the database
export MYSQL_USERNAME=""

# Set your MySQL user password
export MYSQL_PASSWORD=""

# Set the name of the database
export MYSQL_DB=""
export MYSQL_HOST=""

# Set the email of the admin user that will be created in the database
# This user should have the role of admin and should be logged in to access some of the functionalities
export ADMIN_EMAIL=""
export ADMIN_PASSWORD=""

# Set the secret key for the Flask application
# You can generate a secret key by running the following command in the Python shell:
#   import secrets
#   secret_key = secrets.token_hex()  # Generates a 64-character hex string
#   Copy the output of the command and paste it here
export SECRET_KEY=""

export PYTHONPATH=$PYTHONPATH:/home/yasminmahmud/FitJourney/Backend
