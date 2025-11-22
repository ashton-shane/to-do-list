def register_user(get_db, name, username, email, pw_hash):
    cur = get_db().cursor()
    cur.execute("INSERT INTO users (name, username, email, password_hash) VALUES (?,?,?,?)", 
                (name, username, email, pw_hash))
    cur.commit()
    cur.close()

# === DB Helper === #
def query_db(get_db, query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv