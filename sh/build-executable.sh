#!/bin/bash

echo "building executable..."
export GO111MODULE=on

# env CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -a  .

# линкуем статически под линукс
# env CGO_ENABLED=0 GOOS=linux go build -a -ldflags '-extldflags "-static"' -o python/save_articles . 

# CGO_ENABLED=1 нужно для драйвера SQLite
# env CGO_ENABLED=1 GOOS=linux go build -a -ldflags '-linkmode external -extldflags "-static"' .  || exit 1

# echo "Кросскомпиляция в докере. Сделано чтобы компилировать под Windows. 1.15 версия go на момент написания кода."
# docker run --rm -it -v "$PWD":/usr/src/myapp -w /usr/src/myapp -e CGO_ENABLED=1 -e GOOS=linux golang:1.15 go build -a -ldflags '-linkmode external -extldflags "-static"'

# Компиляция под текцщую операционку
env CGO_ENABLED=0 go build -a -ldflags '-extldflags "-static"' -o python/save_articles .