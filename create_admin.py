"""Create the first Admin account.  Run:  python create_admin.py"""
from getpass import getpass

from werkzeug.security import generate_password_hash

from app import get_conn

username = input("Username: ").strip()
email = input("Email: ").strip()
password = getpass("Password: ")
if len(password) < 8:
    raise SystemExit("Password must be at least 8 characters.")

with get_conn() as conn:
    cur = conn.cursor()
    cur.execute("SELECT role_id FROM roles WHERE role_name = 'Admin'")
    row = cur.fetchone()
    if not row:
        raise SystemExit("Role 'Admin' not found. Insert the roles first.")
    cur.execute(
        """INSERT INTO users (role_id, username, email, password_hash)
           VALUES (%s, %s, %s, %s)""",
        (row[0], username, email, generate_password_hash(password)),
    )
print("Admin account created.")
