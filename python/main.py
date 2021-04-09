import os
import sys
import time
import save_rubrics
import save_rubrics_objects
import datetime
import pytz

# время между попытками обновления таблиц
sleep_time = 60 * 5
# счетчик попыток
counter =0

def message_and_sleep():
    dt = datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M:%S')
    print(f'Ждем {sleep_time/60:.0f} минут после обновления # {counter} {dt}...')
    print('----------------------------------\n')
    time.sleep(sleep_time)    


# Повторяем одни и те же действия
while True:
    counter += 1
    print(f'Обновление # {counter}')

    # Обновляем таблицу рубрик
    if not save_rubrics.main():
        print("save_rubrics.main() вернула False.")
        message_and_sleep()
        continue
    
    # Обновляем таблицу связи рубрики-объекты
    if not save_rubrics_objects.main():
        print(f"save_rubrics_objects.main() вернула False.")
        message_and_sleep()
        continue
    
    # Обновляем таблицу статей с помощью вызова go программы.
    path = sys.path[0]
    os.system(path+'/save_articles')
    message_and_sleep()