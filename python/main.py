import os
import sys
import time
import save_rubrics
import save_rubrics_objects

# время между попытками обновления таблиц
sleep_time = 60 * 5
# счетчик попыток
counter =0

# Повторяем одни и те же действия
while True:
    counter += 1
    print(f'Обновление # {counter}')

    # Обновляем таблицу рубрик
    if not save_rubrics.main():
        print(f"save_rubrics.main() вернула False. Ждем {sleep_time/60} мин ...")
        time.sleep(sleep_time)
        continue
    
    # Обновляем таблицу связи рубрики-объекты
    if not save_rubrics_objects.main():
        print(f"save_rubrics_objects.main() вернула False. Ждем {sleep_time/60} мин ...")
        time.sleep(sleep_time)
        continue
    
    # Обновляем таблицу статей с помощью вызова go программы.
    path = sys.path[0]
    os.system(path+'/save_articles')

    print(f'Ждем {sleep_time/60:.0f} минут после обновления # {counter} ...')
    print('----------------------------------\n')
    time.sleep(sleep_time)