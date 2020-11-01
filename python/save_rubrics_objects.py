# сохраняет связи рубрикатор-объект в базе данных
import db
import api
# import sqlite3
import json
import os
import time
import logging


def main():
    "сохраняет связи рубрикатор-объект в базе данных"

    ids = _get_rubric_ids()
    if len(ids)==0:
        print("Не удалось извлечь идентификаторы рубрик из таблицы rubrics")
        return False
    # print(f'Из таблицы rubrics извлечено {len(ids)} идентификаторов рурик')

    n = _create_rubrics_objects_table()
    if n==0 :
        print("Не удалось создать таблицу rubrics_objects_new")
        return False
    # print("Создана таблица rubrics_objects_new")

    
    n = _save_rubrics_objects_to_db(ids)
    if n==0:
        print("Не удалось добавить записи в таблицу rubrics_objects_new")
        return False            
    # print(f'{n} записей добавлены в таблицу rubrics_objects_new за {(time.time()-start)/60:.2f} минут.')

    n = _replace_rubrics_objects_table()
    if n==0:
        print("Не удалось переименовать таблицу rubrics_objects_new")
        return False        
    # print("Таблица rubrics_objects_new переименована в rubrics_objects.")
    # duration = time.time()-start
    # print(f'Создана c {n} записей за {duration/60:.2f} минут. Средняя скорость {n/duration:.2f} объектов/секунду.')

    return True


def _create_rubrics_objects_table():
    "Порождает таблицу rubrics_objects в базе данных."
    
    # Запрос на порождение таблицы
    sql = """
    DROP TABLE IF EXISTS rubrics_objects_new;
    CREATE TABLE IF NOT EXISTS rubrics_objects_new (
        rubric_id TEXT, 
        object_id TEXT,
        datetime TEXT, 
        kind TEXT
        -- PRIMARY KEY(rubric_id, object_id)
    );
    """

    con = db.get_connection()
    n = db.execute(con, sql )
    con.close()
    return n


def _get_rubric_ids():
    "Возвращает рубрики"
    ids = []
    sql = "select id from rubrics"
    records, err, _ = db.execute_and_return(sql)
    ids = [r['id'] for r in records]
    return ids


def _save_rubrics_objects_to_db(ids):    
    "Сохраняет таблицу связи рубрикатора с объектами в базу данных"

    print("rubrics_objects. Считывание объектов рубрик ... ")
    
    rubric_counter=0
    object_counter=0
    start = time.time()
    for id in ids:
        t0 = time.time()
        objects = _get_rubric_objects(id)
        t1 = time.time()
        # Массив для хранения связей рубрика-объект
        links =[]
        for o in objects:
            link = (id, o.get('id'), o.get('datetime'), o.get('kind'))
            links.append(link)

        n = _save_rubric_object_links(links)
        t2 = time.time()
        rubric_counter += 1
        object_counter += len(objects)
        duration = time.time()-start
        rate = object_counter / duration
    #    print('Таблица rubrics_objects ---------------------------------------')
    #    print(f'  В рубрике № {rubric_counter} из {len(ids)} с id={id:6} содержится {len(objects):6} объектов.  Успех сохранения ={n}. Времена загрузки/сохранения = {t1-t0:.2f}/{t2-t1:.2f}')
    #    print(f'  Всего сохранено {object_counter} объектов за {duration/60:.2f} минут. Средняя скорость {rate:.2f} объектов/секунду.')
    
    # print('Таблица rubrics_objects ---------------------------------------')
    print(f' Cохранено {object_counter} объектов за {duration/60:.2f} минут. Средняя скорость {rate:.2f} объектов/секунду.')
    return object_counter


def _get_rubric_objects(rubric_id):
    """
    Получить объекты связанные с рубрикой
    """
    text = api.get_text_from_url(api.url_rubric_objects + rubric_id + '.json')
    try:
        objects = json.loads(text)
    except:
        objects = []
    return objects


def _save_rubric_object_links(links=[]):
    "Сохраняет массив связок (id рубрики - id объекта) в базу данных"
    con = db.get_connection()
    # n = db.executemany_or_by_one(con, "INSERT INTO rubrics_objects_new(rubric_id, object_id, datetime, kind) VALUES (%s,%s,%s,%s)", links)
    n = db.execute_values(con, "INSERT INTO rubrics_objects_new(rubric_id, object_id, datetime, kind) VALUES %s", links, page_size=1000)
    con.close()
    return n


def _replace_rubrics_objects_table():
    "Замещает таблицу rubrics_objects таблицей rubrics_objects_new"

    sql = """
    DROP TABLE IF EXISTS rubrics_objects;
    ALTER TABLE rubrics_objects_new RENAME TO rubrics_objects;
    -- CREATE INDEX rubrics_objects_kind_idx ON rubrics_objects(kind);
    """
    con = db.get_connection()
    n =  db.execute(con, sql )
    con.close()
    return n


if __name__ == "__main__":
    main()
