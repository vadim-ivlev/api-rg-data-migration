import time
import save_rubrics
import save_rubrics_objects

# время между попытками обновления таблиц
sleep_time = 60 * 10
# счетчик попыток
counter =0

# Повторяем одни и те же действия
while True:
    counter += 1
    print(f'Попытка обновления № {counter}')

    # Обновляем таблицу рубрик
    if not save_rubrics.main():
        time.sleep(sleep_time)
        continue
    
    # Обновляем таблицу связи рубрики-объекты
    if not save_rubrics_objects.main():
        time.sleep(sleep_time)
        continue
    
    # Обновляем таблицу статей

    print(f'Ждем {sleep_time/60:.0f} минут после обновления № {counter} ...')
    time.sleep(sleep_time)