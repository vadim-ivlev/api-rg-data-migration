FROM python:3.9.0-slim-buster

# иногда нужно чтобы проверить доступность хостов из контейнера
# RUN apt-get update -y
# RUN apt-get install iputils-ping -y

WORKDIR /usr/src/app

COPY . .
# COPY python/requirements.txt .
RUN pip install --no-cache-dir -r ./python/requirements.txt

CMD [ "python", "-u", "./python/main.py" ]
# CMD [ "sleep", "10000"]
