#!/bin/sh

echo "Updating packages and installing Docker..."
sudo apt update && sudo apt -y install docker.io

echo "Building Docker image..."
docker build -t akenox-inline ~/akenox-inline/

echo "Removing existing container..."
docker rm -f akenox-inline

echo "Running Docker container..."
echo "Send your API ID: "
read API_ID
echo "Send your API HASH: "
read API_HASH
echo "Send your BOT TOKEN: "
read BOT_TOKEN
echo "Send your SESSION STRING: "
read SESSION_STRING
echo "Send your MONGO URL: "
read MONGO_URL
echo "Send your LOG CHANNEL: "
read LOG_CHANNEL

docker run -d --name akenox-inline \
  -e "API_ID=$API_ID" \
  -e "API_HASH=$API_HASH" \
  -e "BOT_TOKEN=$BOT_TOKEN" \
  -e "SESSION_STRING=$SESSION_STRING" \
  -e "MONGO_URL=$MONGO_URL" \
  -e "LOG_CHANNEL=$LOG_CHANNEL" \
  akenox-inline

echo "Viewing logs..."
docker logs -f akenox-inline
