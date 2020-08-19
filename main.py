# Основная программа.
# Считывает данные из API RGRU и сохраняет их в базе данных

import api
import db


db.create_database()
api.get_rubrics()