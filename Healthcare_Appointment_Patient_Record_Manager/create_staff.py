
from getpass import getpass
from app import app
from auth import create_user

username = input("Enter username: ").strip()
password = getpass("Enter password: ")
confirm_password = getpass("Confirm password: ")

print("\nChoose role:")
print("1. Doctor")
print("2. Receptionist")

choice = input("Enter choice (1 or 2): ").strip()

roles = {
    "1": "Doctor",
    "2": "Receptionist",
}

if not username or not password:
    print("Username and password cannot be empty.")
elif password != confirm_password:
    print("Passwords do not match.")
elif choice not in roles:
    print("Invalid role choice.")
else:
    try:
        with app.app_context():
            create_user(username, password, roles[choice])
        print(f"{roles[choice]} account created successfully!")
    except Exception as error:
        print(f"Could not create account: {error}")
