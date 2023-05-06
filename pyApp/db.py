import sqlite3

def connect_db():
    conn = sqlite3.connect('models.db')
    return conn

def create_db_table():
    try:
        conn = connect_db()
        conn.execute('''
            CREATE TABLE models (
                id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                status TEXT NOT NULL,
                urls TEXT NOT NULL,
            );
        ''')
        # id: kdlfgdiugf
        # name: gdgd
        # status: success
        # url: https://localhost.com/static/models/2345343534

        conn.commit()
        print("Model table created successfully")
    except:
        print("Model table creation failed - Maybe table")
    finally:
        conn.close()
