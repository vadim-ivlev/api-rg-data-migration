# сохраняет рубрикатор в базе данных
import db
import api
import sqlite3
import json
import timeit


def main():
    "сохраняет рубрикатор в базе данных"

    print("Creating rubrics table in database...")
    create_rubrics_table()

    print("downloading rubrics...")
    rubrics_json = api.get_text_from_url(api.url_json)
    # timeit.Timer(function).timeit(number=NUMBER)

    print("Saving rubrics to databse...")
    save_rubrics_to_db(rubrics_json)



def create_rubrics_table():
    "Порождает таблицу rubrics в базе данных."
    
    # Запрос на порождение таблицы
    sql_create_rubrics = """
    CREATE TABLE  rubrics (
        id TEXT PRIMARY KEY,
        parent_id TEXT,
        title TEXT,
        uri TEXT
    );
    """
    conn = sqlite3.connect(db.db_filename)
    n =  db.execute(conn, sql_create_rubrics )
    print(f'{n} rubrics table is created')

    conn.close()


# Массив для хранения объектов рубрик перед сохранением в базу данных
rubric_objects = []

def save_rubrics_to_db(text):
    "Сохраняет рубрики в базе данных"
    
    global rubric_objects
    rubric_objects = []
    nodes = json.loads(text)
    
    id = 0
    # Рекурсивно обходим дерево рубрикатора
    for k in nodes.keys():
        # Высший уровень рубрикатора требует особой обработки
        sid = f'{id}-up'
        add_node(None, {'id': sid, 'title': k, 'uri': f'/{k}/'})
        add_nodes(id, nodes[k])
        id += 1
    n = save_rubrics(rubric_objects)
    print(f'{n} out of {len(rubric_objects)} rubrics added')


def add_nodes(parent_id, nodes):
    "Добавляет массив узлов рубрикатора в базу данных"
    for n in nodes:
        add_node(parent_id, n)


def add_node(parent_id, node):   
    "Добавляет узел рубрикатора в базу данных" 
    id = node.get('id')
    o = (id, parent_id, node.get('title'), node.get('uri'))
    rubric_objects.append(o)
    add_nodes(id, node.get('childs',[]))


def save_rubrics(rubrics):
    "Сохраняет рубрики в базу данных"

    conn = sqlite3.connect(db.db_filename)
    sql = "INSERT INTO rubrics VALUES (?,?,?,?)"
    n = db.executemany_or_by_one(conn, sql, rubrics)
    conn.close()
    return n



if __name__ == "__main__":
    main()
