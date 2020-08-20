# Функции обращения к АПИ РГ


import requests
import json
import db

url_proxy = 'https://outer.rg.ru/plain/proxy/?query='

#  url рубрикатора 
url_json = url_proxy + 'https://rg.ru/api/get/rubricator.json'

# url json объектов связанных с рубрикой
url_rubric_objects = url_proxy + 'https://rg.ru/api/get/rubricator/' # + '9.json'


def get_text_from_url(url):
    """
    Возвращает текст из url.
    """    
    r = requests.get(url)
    text = r.text
    r.close()
    return text


# def save_text_to_file(text, file_name):
#     """
#     cохраняет text в файл 
#     """
#     with open(file_name, 'w') as file:
#         file.write(text)
#     return text



# def save_json_to_file(data, file_name):
#     """
#     cохраняет JSON данных в файл
#     """
#     with open(file_name, 'w') as file:
#         json.dump(data, file)

