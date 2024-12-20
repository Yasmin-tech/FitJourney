#!/usr/bin/bash

# Load environment variables
source .env

# Check if all necessary environment variables are set
if [[ -z "$MYSQL_USERNAME" || -z "$MYSQL_PASSWORD" || -z "$MYSQL_DB" || -z "$MYSQL_HOST" ]]; then
  echo "Missing one or more environment variables: MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DB, MYSQL_HOST"
  exit 1
fi


# Prompt for the MySQL root password securely
echo -n "Enter MySQL root password: "
read -s MYSQL_ROOT_PASSWORD
echo

# Run SQL commands to set up the database and user
mysql -u root -p"$MYSQL_ROOT_PASSWORD" -h"$MYSQL_HOST" <<EOF
CREATE DATABASE IF NOT EXISTS $MYSQL_DB;
CREATE USER IF NOT EXISTS '$MYSQL_USERNAME'@'localhost' IDENTIFIED BY '$MYSQL_PASSWORD';
GRANT ALL PRIVILEGES ON $MYSQL_DB.* TO '$MYSQL_USERNAME'@'localhost';
FLUSH PRIVILEGES;
EOF

echo "User and database setup complete."
