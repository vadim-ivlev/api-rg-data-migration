#!/bin/bash


echo "поднимаем" 
docker-compose up -d --build

echo "поясняем"
sh/greetings.sh