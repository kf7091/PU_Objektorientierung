import streamlit as st
from PIL import Image
import json

st.set_page_config(page_title="Benutzeroptionen")

# Überprüft ob Nutzer eingeloggt ist
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Bitte loggen Sie sich zuerst auf der Startseite ein oder erstellen Sie einen neuen Benutzer!")
    st.stop()

st.title("Benutzeroptionen")
# Load user data from JSON file
with open('data/users.json', 'r') as file:
    users = json.load(file)
    # Get current user's username and password
    current_user = st.session_state.logged_in
    username = current_user

    # Allow user to edit username and password
    new_username = st.text_input("Neuer Benutzername")
    new_password = st.text_input("Neues Passwort", type="password")

    # Update user data if new username and password are provided
    if new_username and new_password:
        users[current_user]['username'] = new_username
        users[current_user]['password'] = new_password

        # Save updated user data to JSON file
        with open('data/users.json', 'w') as file:
            json.dump(users, file)

        st.success("Benutzername und Passwort erfolgreich aktualisiert!")
