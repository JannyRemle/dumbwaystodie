"""Add login accounts one by one.   Run:  python create_user.py"""
from getpass import getpass

import pg8000.dbapi
from werkzeug.security import generate_password_hash

from app import get_conn

with get_conn() as conn:
    cur = conn.cursor()
    cur.execute("SELECT role_id, role_name FROM roles ORDER BY role_id")
    roles = cur.fetchall()
if not roles:
    raise SystemExit("The roles table is empty. Insert the roles first.")

while True:
    print("\nRoles:")
    for i, (_, name) in enumerate(roles, 1):
        print(f"  {i}. {name}")
    try:
        role_id = roles[int(input("Choose role number: ")) - 1][0]
    except (ValueError, IndexError):
        print("Invalid choice.")
        continue

    username = input("Username: ").strip()
    email = input("Email: ").strip()
    password = getpass("Password (min 8 characters): ")
    if not username or "@" not in email:
        print("Username and a valid email are required.")
        continue
    if len(password) < 8:
        print("Password is too short.")
        continue
    if password != getpass("Confirm password: "):
        print("Passwords do not match.")
        continue

    try:
        with get_conn() as conn:
            conn.cursor().execute(
                """INSERT INTO users (role_id, username, email, password_hash)
                   VALUES (%s, %s, %s, %s)""",
                (role_id, username, email, generate_password_hash(password)),
            )
        print(f"Created user '{username}'.")
    except pg8000.dbapi.Error as e:
        print("Could not create user (username or email may already exist):", e)

    if input("Add another user? (y/n): ").strip().lower() != "y":
        break
