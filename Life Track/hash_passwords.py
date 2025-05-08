import streamlit_authenticator as stauth

passwords = ['abc123', 'password456']

# Hash each password individually
hashed_passwords = [stauth.Hasher().hash(password) for password in passwords]

print(hashed_passwords)
