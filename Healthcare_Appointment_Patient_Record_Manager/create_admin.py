from getpass import getpass

from app import app
from auth import create_user

username = input("Enter admin username: ").strip()
password = getpass("Enter admin password: ")
confirm_password = getpass("Confirm admin password: ")

if not username or not password:
    print("Username and password cannot be empty.")

elif password != confirm_password:
    print("Passwords do not match.")

else:
    try:
        with app.app_context():
            create_user(username, password, "Administrator")

        print("Administrator account created successfully!")

    except Exception as error:
        print(f"Could not create account: {error}")