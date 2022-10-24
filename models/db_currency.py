import sqlite3

def connectDb():
    connection = sqlite3.connect('db.db')
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS rates(
        date TEXT PRIMARY KEY,
        usd TEXT,
        eur TEXT,
        rub TEXT
        )""")
    return cursor, connection