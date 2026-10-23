"""Sets the password of the 4 sample accounts to Ccsfp@2026 using THIS computer's
Python/Werkzeug, so the stored hash is guaranteed to work.   Run:  python reset_passwords.py"""
from werkzeug.security import check_password_hash, generate_password_hash

from app import get_conn

NEW_PASSWORD = "Ccsfp@2026"
SAMPLE_USERS = ["admin", "dean", "property.officer", "office.head"]

with get_conn() as conn:
    cur = conn.cursor()

    cur.execute("SELECT username, length(password_hash), left(password_hash, 24) FROM users ORDER BY user_id")
    print("Stored hashes BEFORE (length should be 103, start with 'pbkdf2:sha256:1000000'):")
    for username, length, start in cur.fetchall():
        print(f"  {username:<18} length={length:<4} starts with {start}")

    for username in SAMPLE_USERS:
        new_hash = generate_password_hash(NEW_PASSWORD)
        assert check_password_hash(new_hash, NEW_PASSWORD)
        cur.execute(
            "UPDATE users SET password_hash = %s, is_active = TRUE, deleted_at = NULL WHERE username = %s",
            (new_hash, username),
        )
        print(f"  reset {username}: {'updated' if cur.rowcount else 'NOT FOUND'}")

print(f"\nDone. Sign in with any of the 4 usernames and password: {NEW_PASSWORD}")
