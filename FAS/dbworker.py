import sqlite3
import config

def get_current_state(user_id):
    con = sqlite3.connect('./BotDB.db', timeout=2)
    cur = con.cursor()
    cur.execute("SELECT val FROM usrstate WHERE user_id=(" + str(user_id) + ")")
    userval1 = str(cur.fetchone())
    userval = userval1[1:-2]
    con.commit()
    cur.close()
    con.close()
    print(userval)
    return userval

def open_db(db):
    con = sqlite3.connect(db, timeout=2)
    cur = con.cursor()
    return con, cur

def closes_db(con, cur):
    con.commit()
    cur.close()
    con.close()

def set_state(user_id, value):
    con = sqlite3.connect('BotDB.db', timeout=2)
    cur = con.cursor()
    cur.execute("SELECT val FROM usrstate WHERE user_id=" + str(user_id) + "")
    fool = str(cur.fetchone())
    con.commit()
    cur.close()
    con.close()
    if fool == 'None':
        con = sqlite3.connect('./BotDB.db', timeout=2)
        cur = con.cursor()
        print(13)
        cur.execute("INSERT INTO usrstate VALUES(" + str(user_id) + " , " + str(value) + ")")
        con.commit()
        cur.close()
        con.close()
        return True
    else:
        con = sqlite3.connect('./BotDB.db', timeout=2)
        cur = con.cursor()
        print(str(value))
        cur.execute("UPDATE usrstate SET val='" + str(value) + "' WHERE user_id='" + str(user_id) + "'")
        con.commit()
        cur.close()
        con.close()
        return True