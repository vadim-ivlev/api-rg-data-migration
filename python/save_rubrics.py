# сохраняет рубрикатор в базе данных
import db
import api
import json
import time


def main() -> bool:
    "сохраняет рубрикатор в базе данных"

    start = time.time()
    rubrics_json = api.get_text_from_url(api.url_json)
    if rubrics_json == '' or rubrics_json is None:
        print("Не удалось прочитать API: {api.url_json} ")
        return False    
    # print(f'Рубрики загружены из API за {time.time()-start:.2f} sec')


    rubrics = _make_rubrics_list(rubrics_json)
    if len(rubrics) == 0:
        print("Список рубрик в API {api.url_json} пуст")
        return False        
    print(f'Создан список из  {len(rubrics)} рубрик')
    

    n = _create_rubrics_table()
    if n==0:
        print("Не удалось создать таблицу rubrics_new")
        return False        
    print("Созданы таблица rubrics_new")


    start = time.time()
    n = _save_rubrics_to_database(rubrics)
    if n==0:
        print("Не удалось добавить рубрики в таблицу rubrics_new")
        return False            
    print(f'{len(rubrics)} рубрик добавлены в в таблицу rubrics_new за {time.time()-start:.2f} sec.')


    n = _replace_rubrics_table()
    if n==0:
        print("Не удалось переименовать таблицу rubrics_new")
        return False        
    print(f'Таблица rubrics создана с {len(rubrics)} записей за {time.time()-start:.2f} sec.')

    return True



def _create_rubrics_table():
    "Порождает таблицу rubrics в базе данных."
    
    # Запрос на порождение таблицы
    sql_create_rubrics = """
    DROP TABLE IF EXISTS rubrics_new;

    CREATE TABLE rubrics_new (
        id TEXT PRIMARY KEY,
        parent_id TEXT,
        title TEXT,
        uri TEXT
    );
    """
    # con = db.get_connection()
    n =  db.execute(sql_create_rubrics )
    # con.close()
    return n


# Массив для хранения объектов рубрик перед сохранением в базу данных
rubric_objects = []
def _make_rubrics_list(text):
    "Изготавливает массив объетов рубрик"

    # Вспомогательные функции для рекурсивного разбора
    def _add_nodes(parent_id, nodes):
        "Добавляет массив узлов рубрикатора в базу данных"
        for n in nodes:
            _add_node(parent_id, n)

    def _add_node(parent_id, node):   
        "Добавляет узел рубрикатора в базу данных" 
        id = node.get('id')
        o = (id, parent_id, node.get('title'), node.get('uri'))
        rubric_objects.append(o)
        _add_nodes(id, node.get('childs',[]))

    global rubric_objects
    rubric_objects = []
    nodes = json.loads(text)
    
    id = 0
    # Рекурсивно обходим дерево рубрикатора
    for k in nodes.keys():
        # Высший уровень рубрикатора требует особой обработки
        sid = f'{id}-up'
        _add_node(None, {'id': sid, 'title': k, 'uri': f'/{k}/'})
        _add_nodes(id, nodes[k])
        id += 1
    
    return rubric_objects



def _save_rubrics_to_database(rubrics):
    "Сохраняет рубрики в базу данных"

    con = db.get_connection()
    # n = db.executemany_or_by_one(con, "INSERT INTO rubrics_new(id,parent_id,title,uri) VALUES (%s,%s,%s,%s)", rubrics)
    n = db.execute_values(con, "INSERT INTO rubrics_new(id,parent_id,title,uri) VALUES  %s", rubrics, page_size=2000)

    con.close()
    return n


def _replace_rubrics_table():
    "Замещает таблицу rubrics таблицей rubrics_new"

    sql = """
    DROP TABLE IF EXISTS rubrics;
    ALTER TABLE rubrics_new RENAME TO rubrics;
    """
    # con = db.get_connection()
    n =  db.execute(sql )
    # con.close()
    return n



if __name__ == "__main__":
    main()
