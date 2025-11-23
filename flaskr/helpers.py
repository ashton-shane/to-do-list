import re

def validate_field(input, type):
    pattern = None

    # Switchboard to handle different pattern types
    match type:
        case "email": # e.g. "aaa@gmail.com"
            pattern = r"/^[a-zA-Z0–9._%+-]+@[a-zA-Z0–9.-]+\.[a-zA-Z]{2,}$/"
        case "pw": # One special character, one capital letter, one number, min. 8 characters
            pattern = r"^(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$"
        case "user": # min6 max14 alphanumeric chars. No underscores or periods
            pattern = r"[A-Za-z0-9]{6,14}"
    
    #regex validation using fullmatch
    if re.fullmatch(pattern, type):
        return True
    
    return False

def register_user(get_db, username, email, pw_hash, name):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, username, email, password_hash) VALUES (?,?,?,?)", 
                (name, username, email, pw_hash))
    conn.commit()
    cur.close()

# === DB Helper === #
def query_db(get_db, query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv