#!/bin/bash

echo "building ..."
export GO111MODULE=on

# env CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -a  .

# линкуем статически под линукс
# env CGO_ENABLED=0 GOOS=linux go build -a -ldflags '-extldflags "-static"' . 

# CGO_ENABLED=1 нужно для драйвера SQLite
# env CGO_ENABLED=1 GOOS=linux go build -a -ldflags '-linkmode external -extldflags "-static"' .  || exit 1


go build -a -o save_articles .

# echo "Кросскомпиляция в докере. Сделано чтобы компилировать под Windows и Mac. 1.15 версия go на момент написания кода."
# docker run --rm -it -v "$PWD":/usr/src/myapp -w /usr/src/myapp -e CGO_ENABLED=1 -e GOOS=linux golang:1.15 go build -a -ldflags '-linkmode external -extldflags "-static"'

