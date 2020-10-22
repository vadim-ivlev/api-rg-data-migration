import psycopg2
import psycopg2.extras
import logging
import time
import os
# import sqlite3

# Имя файла базы данных
db_filename = 'rg.db'

# DSN = "host=134.0.107.93 port=5432 dbname=rgdb user=root password=rosgas2011"
DSN = os.getenv('RGDSN')

def get_connection():
    try:
        # con = sqlite3.connect(db.db_filename)
        con = psycopg2.connect( DSN )
        return con
    except Exception as ex:
        logging.error(ex)
        return None
    
def execute1(DSN,sql, *args):
    records = None
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
        err = str(ex)
        print("execute error!!! ",err)
    else:
        # print("execute success!!!")
        pass
    finally:
        if "cur" in locals():
            cur.close()
        if "con" in locals():
            con.close()
    return records, err, time.time() - start



def execute(con, query, *argv):
    "Безопасно исполняет запрос"
    try:
        with con:
            cur = con.cursor()
            cur.execute(query, *argv)
            con.commit()
            cur.close()
        return 1
    # except sqlite3.IntegrityError:
    except Exception as exp:
        logging.error(exp)
        return 0



def executemany(con, query, arr=[]):
    """Безопасно исполняет запрос на множестве записей. arr = [(,,),(,,),...].
    Возвращает число вставленных записей"""

    if len(arr) == 0:
        return 0

    try:
        with con:
            cur = con.cursor()
            cur.executemany(query, arr )
            con.commit()
            cur.close()
        return len(arr)
    except Exception:
        return 0



def executemany_or_by_one(con, sql, arr=[]):
    """Если не удается вставить весь массив в базу данных, делает это по одному элементу.
    Возвращает число вставленных елементов"""
    
    n=0
    n = executemany(con, sql, arr)

    if n == 0:
        for e in arr:
            n += execute(con, sql, e) 
    
    return n


if __name__ == "__main__":
    con = get_connection()
    con.close()
