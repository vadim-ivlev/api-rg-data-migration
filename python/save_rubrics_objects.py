# сохраняет связи рубрикатор-объект в базе данных
import db
import api
import sqlite3
import json
import os
import time


def main():
    "сохраняет связи рубрикатор-объект в базе данных"

    create_rubrics_objects_table()
    if n>0:
        print("Создана таблица rubrics_objects_new")

    print("Getting rubric ids ...")
    ids = get_rubric_ids()

    print("Saving rubrics-objects to database...")
    save_rubrics_objects_to_db(ids)


def create_rubrics_objects_table():
    "Порождает таблицу rubrics_objects в базе данных."
    
    # Запрос на порождение таблицы
    sql_create_rubrics_objects = """
    DROP TABLE IF EXISTS rubrics_objects_new;
    DROP INDEX IF EXISTS rubrics_objects_new_kind_idx;

    CREATE TABLE IF NOT EXISTS rubrics_objects_new (
        rubric_id TEXT, 
        object_id TEXT,
        datetime TEXT, 
        kind TEXT,
        PRIMARY KEY(rubric_id, object_id)
    );

    CREATE INDEX rubrics_objects_new_kind_idx ON rubrics_objects_new (kind);
    """
    # sql_create_index = "CREATE INDEX rubrics_objects_new_kind_idx ON rubrics_objects_new (kind);"

    conn = sqlite3.connect(db.db_filename)
    n = db.execute(conn, sql_create_rubrics_objects )
    # n = db.execute(conn, sql_create_index )
    conn.close()
    return n


def get_rubric_ids():
    "Возвращает рубрики"
    conn = sqlite3.connect(db.db_filename)
    # conn.row_factory = sqlite3.Row
    rows = conn.execute("select * from rubrics")  
    ids = [r[0] for r in rows]
    conn.close()
    return ids



def save_rubrics_objects_to_db(ids):
    "Сохраняет таблицу связи рубрикатора с объектами в базу данных"
    
    rubric_counter=0
    object_counter=0

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

        n = save_rubric_object_links(links)
        t2 = time.time()
        print(f'request/saving time = {t1-t0:.2f}/{t2-t1:.2f}')
        file_size = os.path.getsize("rg.db")    
        rubric_counter += 1
        object_counter += len(objects)
        print(f'#rubric N={rubric_counter} rubric id={id}  New objects ={n}/{len(objects)} total objects={object_counter}  file_size={file_size/(1024*1024)}')


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


def save_rubric_object_links(links=[]):
    "Сохраняет массив связок (id рубрики - id объекта) в базу данных"
    conn = sqlite3.connect(db.db_filename)
    n = db.executemany_or_by_one(conn, "INSERT INTO rubrics_objects VALUES (?,?,?,?)", links)
    conn.close()
    print(f'{n} out of {len(links)} rubric-object links saved to database.')
    return n

if __name__ == "__main__":
    main()
