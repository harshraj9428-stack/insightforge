import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(conn, username, password):
    cur = conn.cursor()
    cur.execute(
        "SELECT username, role FROM users WHERE username=? AND password=?",
        (username, hash_password(password))
    )
    return cur.fetchone()
