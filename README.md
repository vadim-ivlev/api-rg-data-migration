# api-data-migration

Цель проекта - миграция данных из API RGRU в базу данных SQLite.


Исполняемый код выкачивает данные из API RGRU и сохраняет их базу данных SQLite rg.rb.
База данных содержит три таблицы:
```
 ribrics       ribrics_objects               articles
 (id)    --<   (rubric_id, object_id)  >---  (obj_id)

```
Названия полей таблиц соответствуют названиям полей данных API.

Исполнение программы
--------------
Исполнение должно выполняться в три этапа в строгой последовательности указанными командами. 
Каждый этап создает и наполняет данными одну таблицу. 

Если установлен Python v>3.7 и Go:

1. `python/1_save_rubrics.py` - сохранение рубрик в таблицу rubrics. (~ 1 тыс. записей)
2. `python/2_save_rubrics_objects.py` - сохранение связей рубрики-объекты в таблицу rubrics_objects. ~3 млн записей.
3. `./save_articles` - сохранение статей в таблицу articles. ~ 1,5 млн записей 



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

 -->
