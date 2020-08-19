# Функции обращения к АПИ РГ


import requests
import re
import json
import os
import time
import db

#  url рубрикатора 
url_xml = 'https://rg.ru/api/get/rubricator.xml'
url_json = 'https://rg.ru/api/get/rubricator.json'

# url json объектов связанных с рубрикой
url_rubric_objects = 'https://rg.ru/api/get/rubricator/' # + '9.json'


def get_text_from_url(url):
    """
    Возвращает текст из url.
    """    
    r = requests.get(url)
    text = r.text
    r.close()
    return text


def save_text_to_file(text, file_name):
    """
    cохраняет text в файл 
    """
    with open(file_name, 'w') as file:
        file.write(text)
    return text

def save_json_to_file(data, file_name):
    """
    cохраняет JSON данных в файл
    """
    with open(file_name, 'w') as file:
        json.dump(data, file)


def extract_rubric_ids(text):
    ids = re.findall(r'id="(\d+)"',text)
    return ids



def get_rubric_objects(rubric_id):
    """
    Получить объекты связанные с рубрикой
    """
    r = requests.get(url_rubric_objects + rubric_id + '.json')
    text = r.text
    r.close()
    try:
        objects = json.loads(text)
    except:
        return []
    return objects

# R U B R I C S ----------------------------------------------------------------------

def save_rubrics_to_db():
    "Сохраняет рубрики в базе данных"
    text = get_text_from_url(url_json)
    nodes = json.loads(text)

    db.new_rubrics_counter = 0
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
    db.save_rubric(id, parent_id, node.get('title'), node.get('uri'))
    add_nodes(id, node.get('childs',[]))


#  RUBRICS-OBJECTS  ------------------------------------------------------------------------


def save_rubrics_objects_to_db(ids):
    "Сохраняет таблицу связи рубрикатора с объектами в базу данных"

    rubric_counter=0
    object_counter=0
    for id in ids:
        objects = get_rubric_objects(id)
        for o in objects:
            # obj_text = json.dumps(o)
            # print(obj_text)
            # with open("objects.json", "a") as myfile:
            #     myfile.write(obj_text +",\n")
            db.save_rubric_object(id, o.get('id'), o.get('datetime'), o.get('kind'))

        file_size = os.path.getsize("rg.db")    
        rubric_counter += 1
        object_counter += len(objects)
        print(rubric_counter, "rubric id=", id, " number of objects = ", len(objects), "total objects=", object_counter, "file_size=", file_size/(1024*1024)  )
        time.sleep(0.1)





# ------------------------------------------------------------------------------------------------------------


# text = get_text_from_url(url_xml)
# save_text_to_file(text, 'rubricator.xml' )
# ids = extract_rubric_ids(text)
# save_json_to_file(ids, 'rubric_ids.json')





# if os.path.exists("objects.json"):
#     os.remove("objects.json")

# with open("objects.json", "a") as myfile:
#     myfile.write("[\n")

# rubric_counter=0
# object_counter=0
# for id in ids:
#     objects = get_rubric_objects(id)
#     for obj in objects:
#         obj_text = json.dumps(obj)
#         # print(obj_text)
#         with open("objects.json", "a") as myfile:
#             myfile.write(obj_text +",\n")

#     file_size = size = os.path.getsize("objects.json")    
#     rubric_counter += 1
#     object_counter += len(objects)
#     print(rubric_counter, "rubric id=", id, " number of objects = ", len(objects), "total objects=", object_counter, "file_size=", file_size/(1024*1024)  )
#     time.sleep(0.1)
#     # input()

# with open("objects.json", "a") as myfile:
#     myfile.write("]\n")

