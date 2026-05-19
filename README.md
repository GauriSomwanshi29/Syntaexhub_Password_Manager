# Syntecxhub Password Manager

A secure local password manager built using Python.

## Features

- Master password authentication
- AES-based encrypted password storage
- Add password entries
- Retrieve passwords
- Search saved credentials
- Delete credentials
- Secure encrypted vault storage

## Technologies Used

- Python
- Cryptography Library
- JSON

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run Project

```bash
python password_manager.py
```

## Project Structure

```text
Syntecxhub_Password_Manager/
│
├── password_manager.py
├── requirements.txt
├── README.md
└── vault.dat
```

## Security

All credentials are encrypted before being stored locally using symmetric encryption.