# сохраняет связи рубрикатор-объект в базе данных
import db
import api
import sqlite3
import json
import os



def main():
    "сохраняет связи рубрикатор-объект в базе данных"

    print("Creating rubrics_objects table in database...")
    create_rubrics_objects_table()

    print("Getting rubric ids ...")
    ids = get_rubric_ids()

    print("Saving rubrics-objects to database...")
    save_rubrics_objects_to_db(ids)


def create_rubrics_objects_table():
    "Порождает таблицу rubrics_objects в базе данных."
    
    # Запрос на порождение таблицы
    sql_create_rubrics_objects = """
    CREATE TABLE  rubrics_objects (
        rubric_id TEXT, 
        object_id TEXT,
        datetime TEXT, 
        kind TEXT,
        PRIMARY KEY(rubric_id, object_id)
    );
    """

    conn = sqlite3.connect(db.db_filename)
    if db.execute(conn, sql_create_rubrics_objects ):
        print('rubrics_objects table is created')
    else:
        print('rubrics_objects table already exists')
    conn.close()


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
        objects = get_rubric_objects(id)
        for o in objects:
            save_rubric_object(id, o.get('id'), o.get('datetime'), o.get('kind'))

        file_size = os.path.getsize("rg.db")    
        rubric_counter += 1
        object_counter += len(objects)
        print(f'#rubric N={rubric_counter} rubric id={id}  number of objects ={len(objects)} total objects={object_counter}  file_size={file_size/(1024*1024)}')




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


new_rubrics_objects_counter =0
def save_rubric_object(rubric_id, object_id, datetime, kind):
    "Сохраняет связку (id рубрики - id объекта) в базу данных"
    global new_rubrics_objects_counter
    conn = sqlite3.connect(db.db_filename)
    if db.execute(conn, "INSERT INTO rubrics_objects VALUES (?,?,?,?)", (rubric_id, object_id, datetime, kind)):
        new_rubrics_objects_counter += 1
        print(f'\nnew rubrics_objects = {new_rubrics_objects_counter}')
    else:
        print(f'rubric_object {rubric_id}-{object_id} exists', end=" ***\r")
    conn.close()


if __name__ == "__main__":
    main()
