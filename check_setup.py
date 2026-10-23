"""Run this FIRST to find out why a login would fail:   python check_setup.py
It checks .env, the database connection, the tables, the roles, and tests the
sample passwords against the stored hashes."""
import sys

from werkzeug.security import check_password_hash

import app as portal

SAMPLE_PASSWORD = "Ccsfp@2026"
EXPECTED_ROLES = {"Admin", "Dean", "Supply and Property Officer", "Office Head"}


def step(ok, text, hint=""):
    print(("  [ OK ] " if ok else "  [FAIL] ") + text)
    if not ok and hint:
        print("         -> " + hint)
    return ok


print("\n1) .env file")
if not step(portal.ENV_FILE.exists(), f"found {portal.ENV_FILE}",
            f"create it by copying .env.example to {portal.ENV_FILE}"):
    sys.exit(1)

print("\n2) Database connection")
try:
    with portal.get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT current_database(), current_user")
        db, user = cur.fetchone()
        step(True, f"connected to database '{db}' as '{user}'")

        print("\n3) Tables")
        cur.execute("SELECT count(*) FROM information_schema.tables "
                    "WHERE table_schema='public' AND table_type='BASE TABLE'")
        n = cur.fetchone()[0]
        if not step(n >= 48, f"{n} tables found (expected 48)",
                    f"you are probably in the wrong database ('{db}'). Run ccsfp_ipms_schema_with_data.sql "
                    "in the database named in DB_NAME"):
            sys.exit(1)

        print("\n4) Roles")
        cur.execute("SELECT role_name FROM roles")
        found = {r[0] for r in cur.fetchall()}
        step(EXPECTED_ROLES <= found, f"roles: {', '.join(sorted(found))}",
             f"missing: {', '.join(sorted(EXPECTED_ROLES - found))}")

        print("\n5) Accounts and passwords")
        cur.execute("SELECT u.username, u.email, u.password_hash, u.is_active, r.role_name "
                    "FROM users u JOIN roles r ON r.role_id = u.role_id "
                    "WHERE u.deleted_at IS NULL ORDER BY u.user_id")
        rows = cur.fetchall()
        if not rows:
            step(False, "no users found", "run the sample data in ccsfp_ipms_schema_with_data.sql")
        for username, email, pw_hash, active, role in rows:
            good = check_password_hash(pw_hash, SAMPLE_PASSWORD)
            note = f"{username:<18} {role:<28} active={active}  password '{SAMPLE_PASSWORD}': {'matches' if good else 'does NOT match'}"
            step(True, note)
except portal.ConfigError as e:
    step(False, str(e))
    sys.exit(1)
except Exception as e:
    reason = e.args[0].get("M") if getattr(e, "args", None) and isinstance(e.args[0], dict) else e
    step(False, f"database error: {reason}",
         "check DB_HOST / DB_PORT / DB_NAME / DB_USER / DB_PASSWORD in .env and that PostgreSQL is running")
    sys.exit(1)

print("\nAll checks done. Start the app with:  python app.py\n")
