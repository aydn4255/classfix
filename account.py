import streamlit as st
import json
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
def app():
    USERS_FILE = 'users.json'

    def load_users():
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_users(users):
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=2)

    def register(username, password):
        users = load_users()

        if username in users:
            st.warning('Username already exists. Please choose another.')
        else:
            hashed_password = generate_password_hash(password, method='sha256')
            user_id = str(uuid.uuid4())
            users[username] = {'password': hashed_password, 'user_id': user_id, 'joined_classes': []}
            save_users(users)
            st.success('Account created successfully! You can now log in.')

    def login(username, password):
        users = load_users()

        if username in users and check_password_hash(users[username]['password'], password):
            st.session_state.user_id = users[username].get('user_id', None)
            return True
        return False


    def main():
        st.title('Login Page')
    
        username = st.text_input('Username:')
        password = st.text_input('Password:', type='password')

        if st.button('Login'):
            if login(username, password):
                st.success('Login successful!')
                
            else:
                st.error('Login failed. Please check your username and password.')

        st.write('Not registered yet')

        new_username = st.text_input('New Username:')
        new_password = st.text_input('New Password:', type='password')

        if st.button('Register'):
            register(new_username, new_password)

    main()