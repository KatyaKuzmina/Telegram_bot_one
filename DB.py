# import sqlite3
#
#
# connection = sqlite3.connect("notes.db")
#
# cursor = connection.cursor()
#
# connection.close()


import sqlite3
from sqlite3 import Error



def sql_connection():
    try:
        connection = sqlite3.connect('notes.db')
        return connection
    except Error:
        print(Error)


def sql_table(con):
    cursorobj = conn.cursor()
    # cursorobj.execute(
    #     "CREATE TABLE employees(id integer PRIMARY KEY, name text, salary real, department text, position text, "
    #     "hireDate text)")
    conn.commit()


conn = sql_connection()
sql_table(conn)
