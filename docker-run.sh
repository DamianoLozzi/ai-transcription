#!/bin/bash

docker build -t ai-assistant . && \
docker run -it -p 8080:8080 ai-assistant ||\
echo -e "\e[31mFailed to build and run the container\e[0m"
