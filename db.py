# Функции роваты с базой данных




def save_rubric(id = 0, parent_id = None, title="", uri=""):
    "Сохраняет рубрику в базу данных"
    print(f'id:{id} parent_id:{parent_id} title:{title} uri:{uri}')