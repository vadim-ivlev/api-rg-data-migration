#!/bin/bash

echo "наполняем директорию deploy"
# rm -rf deploy

rm -rf deploy/python
rm -rf deploy/Dockerfile
rm -rf deploy/docker-compose.yml

cp -R python deploy/
cp -R Dockerfile deploy/
cp -R docker-compose.yml deploy/
