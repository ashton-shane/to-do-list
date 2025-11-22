from . import get_db

def register_user(name, username, email, pw_hash):
    cur = get_db().cursor()
    cur.execute("INSERT INTO users (name, username, email, password_hash) VALUES (?,?,?,?)", 
                name, username, email, pw_hash)
    cur.close()

# === DB Helper === #
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv