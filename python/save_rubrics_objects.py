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
    print(f'Из таблицы rubrics извлечено {len(ids)} идентификаторов рурик')

    n = _create_rubrics_objects_table()
    if n==0 :
        print("Не удалось создать таблицу rubrics_objects_new")
        return False
    print("Создана таблица rubrics_objects_new")

    _save_rubrics_objects_to_db(ids)

    return True

def _create_rubrics_objects_table():
    "Порождает таблицу rubrics_objects в базе данных."
    
    # Запрос на порождение таблицы
    sql = """
    DROP INDEX IF EXISTS rubrics_objects_new_kind_idx;
    DROP TABLE IF EXISTS rubrics_objects_new;

    CREATE TABLE IF NOT EXISTS rubrics_objects_new (
        rubric_id TEXT, 
        object_id TEXT,
        datetime TEXT, 
        kind TEXT
        -- PRIMARY KEY(rubric_id, object_id)
    );

    CREATE INDEX rubrics_objects_new_kind_idx ON rubrics_objects_new (kind);
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
    
    rubric_counter=0
    object_counter=0
    start = time.time()
    for id in ids:
        t0 = time.time()
        objects = get_rubric_objects(id)
        t1 = time.time()
        # Массив для хранения связей рубрика-объект
        links =[]
        for o in objects:
            # save_rubric_object(id, o.get('id'), o.get('datetime'), o.get('kind'))
            link = (id, o.get('id'), o.get('datetime'), o.get('kind'))
            links.append(link)

        n = _save_rubric_object_links(links)
        t2 = time.time()
        # file_size = os.path.getsize("rg.db")    
        rubric_counter += 1
        object_counter += len(objects)
        duration = time.time()-start
        rate = object_counter / duration
        print('--------------------------')
        print(f'#{rubric_counter} rubric_id={id}.  Saved {n} objects out of {len(objects)}.')
        print(f'request/saving time = {t1-t0:.2f}/{t2-t1:.2f}')
        print(f'Total {object_counter} objects in {duration:.2f} sec. Average rate = {rate:.2f} obj/sec.')
    
    return rubric_counter, object_counter, time.time()-start

def get_rubric_objects(rubric_id):
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


if __name__ == "__main__":
    main()
