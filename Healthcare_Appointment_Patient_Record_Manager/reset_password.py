import sqlite3
from getpass import getpass

from app import app
from werkzeug.security import generate_password_hash


username = input("Enter existing username: ").strip()
password = getpass("Enter new password: ")
confirm_password = getpass("Confirm new password: ")

if len(password) < 8:
    print("Password must contain at least 8 characters.")
    raise SystemExit

if password != confirm_password:
    print("Passwords do not match.")
    raise SystemExit

with app.app_context():
    connection = sqlite3.connect(app.config["DATABASE"])

    cursor = connection.execute(
        """
        UPDATE users
        SET password_hash = ?
        WHERE username = ?
        """,
        (generate_password_hash(password), username),
    )

    connection.commit()

    if cursor.rowcount == 1:
        print(f"Password successfully reset for {username}.")
    else:
        print(f"User '{username}' was not found.")

    connection.close()