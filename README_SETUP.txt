CCSFP Integrated Property Management System - login portal
===========================================================
1. Database (pgAdmin)
   - CREATE DATABASE ccsfp_ipms;   (run alone while connected to "postgres")
   - Refresh, click ccsfp_ipms, open Tools > Query Tool (new tab)
   - Run ccsfp_ipms_schema_with_data.sql in that tab

2. Settings
   - Copy .env.example to .env (same folder as app.py) and fill in DB_PASSWORD
   - DB_NAME must be ccsfp_ipms

3. Install (once), from this folder, in your virtual environment:
   pip install -r requirements.txt

4. Check everything BEFORE starting the app:
   python check_setup.py

5. Start:
   python app.py        then open http://127.0.0.1:5000

6. Images: put campus.jpg and logo.png in assets/images/

Sample accounts (password for all: Ccsfp@2026)
   admin              Admin
   dean               Dean
   property.officer   Supply and Property Officer
   office.head        Office Head
You can sign in with the username OR the email (admin@ccsfp.com, etc.).

Add more users:  python create_user.py
