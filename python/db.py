import psycopg2
import psycopg2.extras
import logging
import time
import os
# import sqlite3

# Имя файла базы данных
db_filename = 'rg.db'

DSN = os.getenv('RGDSN')

def get_connection():
    try:
        # con = sqlite3.connect(db.db_filename)
        con = psycopg2.connect( DSN )
        return con
    except Exception as ex:
        logging.error(ex)
        return None
    
def execute_and_return(sql, *args):
    records = []
    err = None    
    start = time.time()
    try:
        con = psycopg2.connect( DSN )
        cur = con.cursor()
        cur.execute(sql, *args)
        con.commit()
        rows = cur.fetchall()
        cols = [x[0] for x in cur.description]
        records = [dict(zip(cols,row)) for row in rows]

    except Exception as ex:
        print(ex)
    finally:
        if "cur" in locals():
            cur.close()
        if "con" in locals():
            con.close()
    return records, err, time.time() - start



def execute(query, *argv):
    "Безопасно исполняет запрос"
    result = 0
    con = get_connection()
    try:
        with con:
            cur = con.cursor()
            cur.execute(query, *argv)
            con.commit()
            cur.close()
            result = 1
    except Exception as ex:
        print(ex)
    finally:
        if "cur" in locals():
            cur.close()
        if "con" in locals():
            con.close()
    return result



# def executemany(con, query, arr=[]):
#     """Безопасно исполняет запрос на множестве записей. arr = [(,,),(,,),...].
#     Возвращает число вставленных записей"""

#     result = 0
#     if len(arr) == 0:
#         return result

#     try:
#         with con:
#             cur = con.cursor()
#             cur.executemany(query, arr )
#             con.commit()
#             result = len(arr)
#     except Exception as ex:
#         print(ex)
#     finally:
#         if "cur" in locals():
#             cur.close()
#         if "con" in locals():
#             con.close()
#     return result


# def executemany_or_by_one(con, sql, arr=[]):
#     """Если не удается вставить весь массив в базу данных, делает это по одному элементу.
#     Возвращает число вставленных елементов"""
    
#     n=0
#     n = executemany(con, sql, arr)

#     if n == 0:
#         for e in arr:
#             n += execute(con, sql, e) 
    
#     return n




def execute_values(con, sql, data=[], template=None, page_size=100, fetch=False):
    """
    this is an example from https://www.psycopg.org/docs/extras.html
    >>> execute_values(cur,
    ... "INSERT INTO test (id, v1, v2) VALUES %s",
    ... [(1, 2, 3), (4, 5, 6), (7, 8, 9)])
    """
    result = 0
    try:
        cur = con.cursor()
        psycopg2.extras.execute_values(cur, sql, data, template=template, page_size=page_size, fetch=fetch)
        con.commit()
        result = 1
    except Exception as ex:
        logging.error(ex)
    finally:
        cur.close()
    return result






if __name__ == "__main__":
    con = get_connection()
    con.close()
