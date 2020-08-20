import sqlite3

# Имя файла базы данных
db_filename = 'rg.db'



def execute(conn, query, *argv):
    "Безопасно исполняет запрос"
    try:
        with conn:
            conn.execute(query, *argv )
        return True
    # except sqlite3.IntegrityError:
    except sqlite3.Error:
        return False



def executemany(conn, query, arr=[]):
    "Безопасно исполняет запрос на множестве записей. arr = [(,,),(,,),...]"
    try:
        with conn:
            conn.executemany(query, arr )
        return True
    # except sqlite3.IntegrityError:
    except sqlite3.Error:
        return False




