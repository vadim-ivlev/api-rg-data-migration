# api-data-migration

Цель проекта - миграция данных из API RGRU в базу данных


## Получение данных

Доступ к API возможен только из внутренней сети rg.

Документация API.
- https://works.rg.ru/project/docs/?section=8

Получить JSON если известен URL материала нужно добавить DATAJSON
как префикс к пути. 
Kamil Ocean, [17.08.20 16:27]
- https://rg.ru/DATAJSON/2020/08/17/reg-pfo/putin-poobeshchal-podderzhat-proizvodstvo-novogo-aviadvigatelia.html

Максим Чагин, [17.08.20 17:13]

- https://rg.ru/xml/yandex/turbo.xml
- https://rg.ru/xml/yandex/turbo-2.xml
- https://rg.ru/xml/yandex/turbo-10.xml

Максим Чагин, [17.08.20 17:25]
- https://rg.ru/api/get/articles/reg-cfo/between-20130201-20130231/index.json

Максим Чагин, [17.08.20 17:25]
- https://rg.ru/api/get/object/by-uri/2013/02/28/reg-cfo/zastrojshik-anons.html.json

Максим Чагин, [17.08.20 17:27]
- https://rg.ru/rf/ - тут можно взять модификаторы для регионов

Максим Чагин, [17.08.20 17:29]
- Можно еще так https://rg.ru/include/tmpl-b-feed/is-announce/num-1000/index.json


## доступ из дома к АПИ

проксирование через сервер у которого есть доступ к этому API
https://outer.rg.ru/plain/proxy/?query=https://rg.ru/api/get/object/article-798781.xml

запрос к rg.ru просто помещаешь в query


<br><br><br>

--------------------------

Порядок работы
==============

1. Изменить код
2. Запустить докер
3. Проверить
4. Запушить
5. Отдеплоить


Команды
-------
В директории `sh/` находятся следующие команды для облегчения работы.


|   |   |
|---|---|
Подъем                                      | `sh/up.sh`
Приостановка контейнера                     | `sh/stop.sh`
Старт приостановленного контейнера          | `sh/start.sh`
Полный останов контейнера                   | `sh/down.sh`
Подготовка директории deploy                | `sh/build-deploy-directory.sh`
Деплой                                      | `sh/deploy.sh`



Перезапуск Caddy и перестройка контейнера если что то изменилость в docker-compose
```
dc restart log-monitor-caddy
dc up -d --build log-monitor-caddy
```
