# сохраняет рубрикатор в базе данных
import db
import api
import sqlite3
import json


def main():
    "сохраняет рубрикатор в базе данных"
    create_rubrics_table()
    save_rubrics_to_db()



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
    if db.execute(conn, sql_create_rubrics ):
        print('rubrics table is created')
    else:
        print('rubrics table already exists')

    conn.close()



# R U B R I C S ----------------------------------------------------------------------

new_rubrics_counter =0

def save_rubrics_to_db():
    "Сохраняет рубрики в базе данных"
    
    global new_rubrics_counter
    new_rubrics_counter = 0

    text = api.get_text_from_url(api.url_json)
    nodes = json.loads(text)
    
    id = 0
    # Рекурсивно обходим дерево рубрикатора
    for k in nodes.keys():
        # Высший уровень рубрикатора требует особой обработки
        sid = f'{id}-up'
        add_node(None, {'id': sid, 'title': k, 'uri': f'/{k}/'})
        add_nodes(id, nodes[k])
        id += 1



def add_nodes(parent_id, nodes):
    "Добавляет массив узлов рубрикатора в базу данных"
    for n in nodes:
        add_node(parent_id, n)


def add_node(parent_id, node):   
    "Добавляет узел рубрикатора в базу данных" 
    id = node.get('id')
    save_rubric(id, parent_id, node.get('title'), node.get('uri'))
    add_nodes(id, node.get('childs',[]))



def save_rubric(id = 0, parent_id = None, title="", uri=""):
    "Сохраняет рубрику в базу данных"
    global new_rubrics_counter
    conn = sqlite3.connect(db.db_filename)
    if db.execute(conn, "INSERT INTO rubrics VALUES (?,?,?,?)", (id,parent_id,title,uri)):
        new_rubrics_counter += 1
        print(f'\nnew rubrics = {new_rubrics_counter}')
    else:
        print(f'rubric {id} exists', end=" ***\r")
    conn.close()


if __name__ == "__main__":
    main()
