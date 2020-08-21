#!/bin/bash

echo "building ..."
export GO111MODULE=on

# env CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -a  .

# линкуем статически под линукс
# env CGO_ENABLED=0 GOOS=linux go build -a -ldflags '-extldflags "-static"' . 

# CGO_ENABLED=1 нужно для драйвера SQLite
env CGO_ENABLED=1 GOOS=linux go build -a -ldflags '-linkmode external -extldflags "-static"' .  || exit 1

