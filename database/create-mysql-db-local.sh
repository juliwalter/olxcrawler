#!/bin/sh

# Set the script to exit on any error
set -e

# Function to print a loading bar
print_loading_bar() {
  local progress=$1
  local bar_length=20
  local completed_length=$((progress * bar_length / 100))
  local remaining_length=$((bar_length - completed_length))

  printf "["
  for ((i = 0; i < completed_length; i++)); do
    printf "="
  done
  printf ">"
  for ((i = 0; i < remaining_length; i++)); do
    printf "."
  done
  printf "] %d%%\r" "$progress"
}

# variables
MYSQL_VERSION=8.0.19
PORT=3306
CONTAINER_NAME=olxcrawler-db-local
DATABASE_NAME=olxcrawler
ROOT_USER=root
ROOT_PASSWORD=admin
DEV_USER=dev
DEV_PASSWORD=dev

# Check if the database already exists
existing_database=$(docker ps -q -f name=$CONTAINER_NAME)

if [ -n "$existing_database" ]; then
  # Ask the user if the database should be deleted
  echo "The database '$DATABASE_NAME' already exists. Do you want to delete it and create a new one? (y/n): "
  read answer

  if [ "$answer" == "y" ]; then
    # Stop and remove existing Docker container with the same name
    docker stop $CONTAINER_NAME > /dev/null 2>&1 || true
    docker rm $CONTAINER_NAME > /dev/null 2>&1 || true
    echo "Existing database removed."
  else
    echo "Existing database will not be removed. Exiting."
    exit 0
  fi
fi

# Start to run docker container
if docker run -d \
  --name=$CONTAINER_NAME \
  -p $PORT:$PORT \
  -e MYSQL_ROOT_PASSWORD=$ROOT_PASSWORD \
  -e MYSQL_DATABASE=$DATABASE_NAME \
  -t mysql:$MYSQL_VERSION \
  --default-authentication-plugin=mysql_native_password > /dev/null 2>&1;then
  echo "Created new container"
else
  echo "Failed to create container"
  exit 1
fi

SLEEP_TIME=30
echo "Wait for the database to be started: "
for i in $(seq 1 $SLEEP_TIME); do
  progress=$((i * 100 / SLEEP_TIME))
  print_loading_bar "$progress"
  sleep 1
done

echo "\nFinished waiting"

# Create Dev user
if docker exec $CONTAINER_NAME bash -c \
  "mysql -hlocalhost -P 3306 -u$ROOT_USER -p$ROOT_PASSWORD -e \"CREATE USER '$DEV_USER'@'%' IDENTIFIED WITH mysql_native_password BY '$DEV_PASSWORD'; GRANT ALL PRIVILEGES ON *.* TO '$DEV_USER'@'%' WITH GRANT OPTION; FLUSH PRIVILEGES;\"" > /dev/null 2>&1; then
  echo "Successfully created dev user"
else
  echo "Failed to create dev user"
  exit 1
fi
