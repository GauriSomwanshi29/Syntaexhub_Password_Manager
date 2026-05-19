import json
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

VAULT_FILE = "vault.dat"

# Generate encryption key from master password
def generate_key(master_password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )

    key = base64.urlsafe_b64encode(
        kdf.derive(master_password.encode())
    )

    return key

# Load vault
def load_vault(master_password):
    if not os.path.exists(VAULT_FILE):
        return {}, os.urandom(16)

    with open(VAULT_FILE, "rb") as file:
        salt = file.read(16)
        encrypted_data = file.read()

    key = generate_key(master_password, salt)
    fernet = Fernet(key)

    try:
        decrypted_data = fernet.decrypt(encrypted_data)
        data = json.loads(decrypted_data.decode())
        return data, salt

    except:
        print("Wrong master password!")
        return None, None

# Save vault
def save_vault(data, master_password, salt):
    key = generate_key(master_password, salt)
    fernet = Fernet(key)

    encrypted_data = fernet.encrypt(
        json.dumps(data).encode()
    )

    with open(VAULT_FILE, "wb") as file:
        file.write(salt)
        file.write(encrypted_data)

# Add password
def add_password(data):
    site = input("Enter site/app name: ")
    username = input("Enter username: ")
    password = input("Enter password: ")

    data[site] = {
        "username": username,
        "password": password
    }

    print("Password added successfully!")

# Retrieve password
def retrieve_password(data):
    site = input("Enter site name: ")

    if site in data:
        print("\nSaved Credentials:")
        print("Username:", data[site]["username"])
        print("Password:", data[site]["password"])
    else:
        print("No entry found!")

# Search password
def search_password(data):
    keyword = input("Search website/app: ")

    found = False

    for site in data:
        if keyword.lower() in site.lower():
            print("\nFound:", site)
            found = True

    if not found:
        print("No matching entries!")

# Delete password
def delete_password(data):
    site = input("Enter site name to delete: ")

    if site in data:
        del data[site]
        print("Entry deleted!")
    else:
        print("No entry found!")

# Main menu
def main():
    print("===== PASSWORD MANAGER =====")

    master_password = input("Enter master password: ")

    data, salt = load_vault(master_password)

    if data is None:
        return

    while True:
        print("\n1. Add Password")
        print("2. Retrieve Password")
        print("3. Search Password")
        print("4. Delete Password")
        print("5. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            add_password(data)
            save_vault(data, master_password, salt)

        elif choice == "2":
            retrieve_password(data)

        elif choice == "3":
            search_password(data)

        elif choice == "4":
            delete_password(data)
            save_vault(data, master_password, salt)

        elif choice == "5":
            print("Exiting Password Manager...")
            break

        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()