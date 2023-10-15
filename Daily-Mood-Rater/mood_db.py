import sqlite3
from datetime import datetime
from pathlib import Path

cur_dir = Path.cwd()

try:
    connection = sqlite3.connect(cur_dir / "src/mood.db")
except Exception as err:
    print("\033[1;37;40mThe application faced a problem while trying to create or connect to the database:\033[0;37;40m")
    print("\033[1;31;40m", err, "\033[0;37;40m")
    import sys
    sys.exit()

cursor = connection.cursor()

def create_table():
    with connection:
        cursor.execute("""CREATE TABLE moods (
            mood INTEGER,
            description TEXT,
            date TEXT
            )""")

def save_values(mood:int, description=" "):
    with connection:
        cursor.execute("SELECT * FROM moods WHERE date = :date", {"date":str(datetime.now())[:10]})
        result = cursor.fetchone()
        # If there is no entry matching the current date:
        if result is None:
            cursor.execute(
                "INSERT INTO moods VALUES (:mood, :desc, :date)", 
                {"mood":mood, "desc":description, "date":str(datetime.now())[:10]})
            # If an entry is succesfully insterted, let the method of the app know by returning 1
            return 1
        else:
            return result

def update_values(mood:int, description=""):
    with connection:
        cursor.execute("""UPDATE moods 
                        SET mood = :mood,
                        description = :desc
                        WHERE date = :today""",
                        {"mood":mood, "desc":description, "today":str(datetime.now())[:10]})

def show_values(date):
    cursor.execute("""SELECT * FROM moods
                    WHERE SUBSTR(date, 1, 7) == :date
                    ORDER BY date""",
                    {"date":date})
    result = cursor.fetchall()

    return result

def current_months():
    cursor.execute("SELECT DISTINCT SUBSTR(date, 1, 7) FROM moods ORDER BY date")
    result = cursor.fetchall()

    return result

try:
    create_table()
except sqlite3.OperationalError as err:
    pass
except Exception as err:
    print("\033[1;37;40mPreviously uncaught exception for creating table! Please let me know about this:")
    print("\033[1;31;40m", err, "\033[0;37;40m")

