# Основная программа.
# Считывает данные из API RGRU и сохраняет их в базе данных

import api
import db


db.create_database()
# api.save_rubrics_to_db()
ids = db.get_rubric_ids()
api.save_rubrics_objects_to_db(ids)