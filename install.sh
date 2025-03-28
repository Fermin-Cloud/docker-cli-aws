#!/bin/bash

error_exit() {
    echo "Error: $1"
    exit 1
}

command -v docker &> /dev/null || error_exit "Docker is not installed"
docker info &> /dev/null || error_exit "Docker is not running"
[ -f "Dockerfile" ] || error_exit "No Dockerfile found in the current directory."
[ -w "." ] || error_exit "You do not have write permissions in the current directory"
[ -f ".env" ] || echo "The .env file was not found"

# it
read -p "Are you sure you want to build the Docker image? 'aws-cli'? (s/n): " confirm
if [[ ! "$confirm" =~ ^[sS]$ ]]; then
    echo "Process canceled by the user"
    exit 0
fi

echo "Building the Docker image 'aws-cli'..."
docker build -t aws-cli .

# valid building
if [ $? -eq 0 ]; then
    echo "The 'aws-cli' image was built successfully!"
else
    echo "Error: There was a problem building the image."
    exit 1
fi

# docker build -t aws-translate .
# docker run -p 8000:8000 --env-file .env aws-translate
# curl -X POST "http://localhost:8000/translate/" -H "Content-Type: application/json" -d '{"text":"Hola","source_language":"es","target_language":"en"}'