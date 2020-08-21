#!/bin/bash

echo "build a docker image"
docker build -t vadimivlev/datascience-notebook-plus:latest -f Dockerfile-datascience . 

echo "push the docker image" 
docker login
docker push vadimivlev/datascience-notebook-plus:latest

