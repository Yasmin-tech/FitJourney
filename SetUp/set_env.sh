#!/bin/bash

# Set up the default environment variables
echo "Setting up environment variables..."
export MYSQL_USERNAME="fit_journey_user"
export MYSQL_PASSWORD="fit_journey_password"
export MYSQL_DB="FitJourney"
export MYSQL_HOST="localhost"

export ADMIN_EMAIL="admin@exaample.com"
export ADMIN_PASSWORD="adminpassword"

# unset ADMIN_EMAIL
# unset ADMIN_PASSWORD

export SECRET_KEY="ed5de5c8d6448e9e5d6b9ffbdb5335bed33577fe2bbfa863333a194e9611f6ac"

export PYTHONPATH=$PYTHONPATH:/home/yasminmahmud/FitJourney/Backend
