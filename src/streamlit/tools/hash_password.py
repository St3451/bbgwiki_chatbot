"""
Password Hashing Utility for Streamlit Authenticator

This script is intended to be run manually to:
1. Hash a plain-text password for use in `config_users.yaml`.
2. Generate a secure random cookie key used for signing session cookies.

This is useful when setting up authentication with the `streamlit-authenticator` library.

Usage:
    python tools/hash_password.py

Notes:
- Replace the `password` variable with your actual password before running.
- The printed cookie key should be placed in the `key` field of your YAML config.
"""

    
import secrets
import streamlit_authenticator as stauth

def main():
    password = 'pass_bbgwiki'  # Replace with your actual password
    hasher = stauth.Hasher()
    hashed_password = hasher.hash(password)
    print(f"\nPassword: {password}")
    print(f"Hashed password: {hashed_password}")
    print(f"Cookie key: {secrets.token_hex(16)}")

if __name__ == "__main__":
    main()