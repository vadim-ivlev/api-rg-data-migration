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
    objects = json.loads(text)
    return objects

# R U B R I C S ----------------------------------------------------------------------

def get_rubrics():
    text = get_text_from_url(url_json)
    nodes = json.loads(text)

    id = 0
    for k in nodes.keys():
        # Высший уровень рубрикатора требует особой обработки
        sid = f'upper{k}'
        add_node(None, {'id': sid, 'title': k, 'uri': f'/{k}/'})
        add_nodes(id, nodes[k])
        id += 1



def add_nodes(parent_id, nodes):
    for n in nodes:
        add_node(parent_id, n)


def add_node(parent_id, node):    
    id = node.get('id')
    title = node.get('title')
    uri = node.get('uri')
    childs = node.get('childs',[])
    db.save_rubric(id,parent_id,title,uri)
    add_nodes(id, childs )





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

