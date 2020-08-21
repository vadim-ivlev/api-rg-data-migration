#!/bin/bash



echo "Starting stopped containers..."

docker-compose start

# поясняем
sh/greetings.sh
