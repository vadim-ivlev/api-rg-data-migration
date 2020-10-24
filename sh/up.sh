#!/bin/bash

echo "поднимаем приложение" 
docker-compose up -d --build

echo "поясняем"
sh/greetings.sh