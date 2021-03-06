FROM python:3.9.0-slim-buster

# иногда нужно чтобы проверить доступность хостов из контейнера
# RUN apt-get update -y
# RUN apt-get install iputils-ping -y

WORKDIR /usr/src/app

COPY python/. .
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "-u", "main.py" ]
# CMD [ "sleep", "10000"]
