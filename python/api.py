# Функции обращения к АПИ РГ


import requests
import json
import os

request_timeout = float(os.getenv('REQUEST_TIMEOUT', "5.0"))
print(f"REQUEST_TIMEOUT = {request_timeout}")

url_proxy = 'https://outer.rg.ru/plain/proxy/?query='

#  url рубрикатора 
url_json = url_proxy + 'https://rg.ru/api/get/rubricator.json'

# url json объектов связанных с рубрикой
url_rubric_objects = url_proxy + 'https://rg.ru/api/get/rubricator/' # + '9.json'


def get_text_from_url(url):
    """
    Возвращает текст из url.
    """    
    text = ""
    try:
        r = requests.get(url, timeout = request_timeout)
        text = r.text
        r.close()  
    except Exception as ex:
        print(f"REQUEST ERROR ----> {url}")
        # print(ex)

    return text


