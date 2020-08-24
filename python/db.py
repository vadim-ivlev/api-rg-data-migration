import sqlite3

# Имя файла базы данных
db_filename = 'rg.db'



def execute(conn, query, *argv):
    "Безопасно исполняет запрос"
    try:
        with conn:
            conn.execute(query, *argv )
        return 1
    # except sqlite3.IntegrityError:
    except sqlite3.Error:
        return 0



def executemany(conn, query, arr=[]):
    """Безопасно исполняет запрос на множестве записей. arr = [(,,),(,,),...].
    Возвращает число вставленных записей"""

    if len(arr) == 0:
        return 0

    try:
        with conn:
            conn.executemany(query, arr )
        return len(arr)
    except sqlite3.Error:
        return 0



def executemany_or_by_one(conn, sql, arr=[]):
    """Если не удается вставить весь массив в базу данных, делает это по одному элементу.
    Возвращает число вставленных елементов"""
    
    n = executemany(conn, sql, arr)

    if n == 0:
        for e in arr:
            n += execute(conn, sql, e) 
    
    return n


