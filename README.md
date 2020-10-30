# api-data-migration

Цель проекта - миграция данных из API RGRU в базу данных SQLite. 
Это часть проекта по автоматическому формированию врезок к материалам RG.

## Результат

Можно скачать здесь: <https://1drv.ms/u/s!AmtnhvXAi-RmgoQuuTUD4gdrYrJPyA?e=L4175E> 
(Пароль: rosg******)

Описание программы
-----------
Исполняемый код выкачивает данные из API RGRU и сохраняет их базу данных SQLite rg.rb.
База данных содержит три таблицы:
```
 ribrics       ribrics_objects               articles
 (id)    --<   (rubric_id, object_id)  >---  (obj_id)

```
```sql
> sqlite-utils tables --table --counts  --schema rg.db

table              count  schema
---------------  -------  -----------------------------------------
rubrics             1153  CREATE TABLE rubrics (
                                  id TEXT PRIMARY KEY,
                                  parent_id TEXT,
                                  title TEXT,
                                  uri TEXT
                              )
rubrics_objects  3053116  CREATE TABLE rubrics_objects (
                                  rubric_id TEXT,
                                  object_id TEXT,
                                  datetime TEXT,
                                  kind TEXT,
                                  PRIMARY KEY(rubric_id, object_id)
                              )
articles         1202159  CREATE TABLE articles(
                                        obj_id TEXT PRIMARY KEY,
                                        announce TEXT,
                                        authors TEXT,
                                        date_modified TEXT,
                                        "full-text" TEXT,
                                        images TEXT,
                                        index_priority TEXT,
                                        is_active TEXT,
                                        is_announce TEXT,
                                        is_paid TEXT,
                                        link_title TEXT,
                                        links TEXT,
                                        obj_kind TEXT,
                                        projects TEXT,
                                        release_date TEXT,
                                        spiegel TEXT,
                                        title TEXT,
                                        uannounce TEXT,
                                        url TEXT,
                                        migration_status TEXT DEFAULT ''
                                )

```


Названия полей таблиц соответствуют названиям полей данных API.

Исполнение программы
--------------
Исполнение должно выполняться в три этапа в строгой последовательности указанными командами. 
Каждый этап создает и наполняет данными одну таблицу. 

Если установлен python v>3.7 и Go выполните `pip install -r python/requirements.txt`, а затем:

1. `python/1_save_rubrics.py` - сохранение рубрик в таблицу rubrics. (~ 1 тыс. записей)
2. `python/2_save_rubrics_objects.py` - сохранение таблицы связей rubrics_objects. ~3 млн записей.
3. `./save_articles` - сохранение статей в таблицу articles. ~ 1,5 млн записей 

Если python не установлен, но есть docker:

1. `docker run --rm  -v "$PWD:/app" -w "/app" python:3.7-alpine  sh -c "pip install -r python/requirements.txt && python python/1_save_rubrics.py"`
2. `docker run --rm  -v "$PWD:/app" -w "/app" python:3.7-alpine  sh -c "pip install -r python/requirements.txt && python python/1_save_rubrics_objects.py"`
3. `./save_articles` 

**Примечание**: Исполнямый файл `save_articles` создается командой `./build.sh`,
Если на компьютере установлен go. можно запустить программу и без компиляции командой `go run *.go`. 
Исполнение может занять несколько часов, размер файла базы данных составит около 9Гб.




## Об API

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



Проксирование, для доступа из дома

https://outer.rg.ru/plain/proxy/?query=https://rg.ru/api/get/object/article-798781.xml

запрос к rg.ru поместить в query

<!-- 
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



drwxrwxr-x  2 gitupdater gitupdater 4.0K Oct  9 03:54 cvs/
-rwxrwxr-x  1 gitupdater gitupdater 2.8G Oct 20 15:29 cvs.zip*
drwxrwxr-x  6 gitupdater gitupdater 4.0K Oct 20 14:42 data-migrations/
drwxrwxr-x 10 gitupdater gitupdater 4.0K Oct 22 01:59 rg-corpus/
-rwxrwxr-x  1 gitupdater gitupdater 7.5G Oct 20 03:54 rg-corpus.zip*
drwxrwxr-x  3 gitupdater gitupdater 4.0K Oct 20 13:02 rg-db/
-rwxrwxr-x  1 gitupdater gitupdater 4.8G Oct 20 03:14 rg-db.zip*
drwxrwxr-x  9 gitupdater gitupdater 4.0K Oct 20 17:41 text-processor/
drwxrwxr-x  9 gitupdater gitupdater 4.0K Oct 13 19:12 text-processor0/
-rwxrwxr-x  1 gitupdater gitupdater 678K Oct 20 03:52 text-processor.zip*

ALTER TABLE <table> ALTER COLUMN <column> DROP DEFAULT;

 -->
