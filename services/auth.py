import hashlib

def authenticate(conn, username, password):
    if conn is None:
        return None

    cur = conn.cursor()
    hashed = hashlib.sha256(password.encode()).hexdigest()

    cur.execute(
        "SELECT username, role FROM users WHERE username=? AND password=?",
        (username, hashed)
    )

    return cur.fetchone()
