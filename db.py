# Функции роваты с базой данных


import sqlite3

# Имя файла базы данных
db_filename = 'rg.db'

# Запросы на порождение таблиц
sql_create_rubrics = """
CREATE TABLE  rubrics (
    id TEXT PRIMARY KEY,
    parent_id TEXT,
    title TEXT,
    uri TEXT
);
"""
sql_create_rubrics_objects = """
CREATE TABLE  rubrics_objects (
    rubric_id TEXT, 
    object_id TEXT,
    datetime TEXT, 
    kind TEXT,
    PRIMARY KEY(rubric_id, object_id)
);
"""


def execute(conn, query, *argv):
    "Безопасно исполняет запрос"
    try:
        with conn:
            conn.execute(query, *argv )
        return True
    # except sqlite3.IntegrityError:
    except sqlite3.Error:
        return False


def create_database():
    conn = sqlite3.connect(db_filename)

    if execute(conn, sql_create_rubrics ):
        print('rubrics table is created')
    else:
        print('rubrics table already exists')

    if execute(conn, sql_create_rubrics_objects ):
        print('rubrics_objects table is created')
    else:
        print('rubrics_objects table already exists')

    conn.close()



new_rubrics_counter =0
def save_rubric(id = 0, parent_id = None, title="", uri=""):
    "Сохраняет рубрику в базу данных"
    global new_rubrics_counter
    conn = sqlite3.connect(db_filename)
    if execute(conn, "INSERT INTO rubrics VALUES (?,?,?,?)", (id,parent_id,title,uri)):
        new_rubrics_counter += 1
        print(f'\nnew rubrics = {new_rubrics_counter}')
    else:
        print(f'rubric {id} exists', end=" ***\r")
    conn.close()



def get_rubric_ids():
    "Возвращает рубрики"
    conn = sqlite3.connect(db_filename)
    # conn.row_factory = sqlite3.Row
    rows = conn.execute("select * from rubrics")  
    ids = [r[0] for r in rows]
    conn.close()
    return ids


new_rubrics_objects_counter =0
def save_rubric_object(rubric_id, object_id, datetime, kind):
    "Сохраняет связку (id рубрики - id объекта) в базу данных"
    global new_rubrics_objects_counter
    conn = sqlite3.connect(db_filename)
    if execute(conn, "INSERT INTO rubrics_objects VALUES (?,?,?,?)", (rubric_id, object_id, datetime, kind)):
        new_rubrics_objects_counter += 1
        print(f'\nnew rubrics_objects = {new_rubrics_objects_counter}')
    else:
        print(f'rubric_object {rubric_id}-{object_id} exists', end=" ***\r")
    conn.close()

