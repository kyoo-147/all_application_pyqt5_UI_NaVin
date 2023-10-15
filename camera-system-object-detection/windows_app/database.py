import sqlite3

def createTrigger(trigger):
    conn = sqlite3.connect('Triggers.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO triggers values (?,?,?,?,?,?,?,?,?)', (
                    trigger.name,
                    trigger.initialTime,
                    trigger.finalTime,
                    trigger.maxStayTime,
                    trigger.action,
                    trigger.areaStartX,
                    trigger.areaStartY,
                    trigger.areaEndX,
                    trigger.areaEndY))

    trigger.id = cursor.lastrowid

    conn.commit()
    conn.close()

def selectTriggers():
    conn = sqlite3.connect('Triggers.db')
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='triggers'")
    if len(cursor.fetchall()) == 0:
        cursor.execute('CREATE TABLE triggers(name text, timeFrom text, timeTo text, stayTime integer, action text, areaStartX integer, areaStartY integer, areaEndX integer, areaEndY integer)')

    cursor.execute('SELECT rowid, * FROM triggers')
    rows = cursor.fetchall()

    conn.close()

    return rows

def deleteTrigger(id):
    conn = sqlite3.connect('Triggers.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM triggers WHERE rowid = ?', (id,))

    conn.commit()
    conn.close()

def printDB():
    print('------------------DB------------------')
    for row in selectTriggers():
        print(row)