# Функции роваты с базой данных


import sqlite3

db_filename = 'rg.db'

# Запросы на порождение таблиц
sql_create_tables = """
CREATE TABLE IF NOT EXISTS rubrics (
    id TEXT PRIMARY KEY,
    parent_id TEXT,
    title TEXT,
    uri TEXT
);
"""


def create_database():
    conn = sqlite3.connect(db_filename)
    c = conn.cursor()
    c.execute(sql_create_tables)
    conn.commit()
    conn.close()




def save_rubric(id = 0, parent_id = None, title="", uri=""):
    "Сохраняет рубрику в базу данных"
    print(f'id:{id} parent_id:{parent_id} title:{title} uri:{uri}')

    conn = sqlite3.connect(db_filename)
    c = conn.cursor()
    c.execute("INSERT INTO rubrics VALUES (?,?,?,?)", (id,parent_id,title,uri) )
    conn.commit()
    conn.close()
