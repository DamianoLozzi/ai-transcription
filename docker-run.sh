#!/bin/bash

docker build --progress=plain -t ai-assistant . && \
docker run -it ai-assistant ||\
echo -e "\e[31mFailed to build and run the container\e[0m"
