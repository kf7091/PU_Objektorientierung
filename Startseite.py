import streamlit as st
from PIL import Image
import json

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

# Benutzerdaten aus einer JSON Datei laden
def load_users(file_path='data/users.json'):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Benutzerdaten in eine JSON Datei speichern
def save_users(users, file_path='data/users.json'):
    with open(file_path, 'w') as file:
        json.dump(users, file)

# Benutzerdaten laden
users = load_users()

# Überprüft ob Benutzername und Passwort mit einem vorhandenen Benutzer im System übereinstimmen.
def login(username, password):

    if username in users and users[username] == password:
        return True
    return False

# Legt einen neuen Benutzer an
def register(username, password):
    if username in users:
        return False
    users[username] = password
    save_users(users)
    return True

# Session State wird leer angelegt, solange er noch nicht existiert
# Überprüft ob Nutzer eingeloggt ist
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# Start der Startseite und Überschrift
st.title("Schauen Sie Ihre EKD-Daten an!")
# Bild und Text nebeneinander anzeigen
#st.columns([10,1,10,20])
#col1,col2 = st.columns([2,2])

#with col1:
#    try:
#        logo = Image.open('data/pictures/Logo.png')
#        st.image(logo, caption='', width=logo.width // 1)
#    except Exception as e:
#        st.error(f"Logo konnte nicht geladen werden: {e}")
#with col2:
st.write("Willkommen zur EKG-Datenanalyse-App!")
st.write("Um Ihre Daten analysieren zu können müssen Sie sich einloggen.")
st.write("Falls Sie noch keinen Account haben, registrieren Sie sich bitte.")

# Login und Registrierungsformular nebeneinander anzeigen
col1,col2 = st.columns(2)

with col1:
    if not st.session_state.logged_in:
        st.title("Login")
        username = st.text_input("Benutzername")
        password = st.text_input("Passwort", type="password")
        
        if st.button("Login"):
            if login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Erfolgreich eingeloggt!")
                st.experimental_rerun()  # Neuladen der Anwendung für sichtbare Änderungen
            else:
                st.error("Ungültige Anmeldeinformationen")
with col2:       
    # Registrierungsformular
    if not st.session_state.logged_in:
        st.title("Registrieren")
        reg_username = st.text_input("Neuer Benutzername")
        reg_password = st.text_input("Neues Passwort", type="password")
        
        if st.button("Registrieren"):
            if register(reg_username, reg_password):
                st.success("Sie sind nun registriert! Bitte loggen Sie sich ein")
            else:
                st.error("Dieser Benutzername existiert bereits. Bitte wählen Sie einen anderen Benutzernamen.")

# Inhalt anzeigen nach erfolgreichen Login
left,col1 = st.columns([0.5,2])

with col1:
    if st.session_state.logged_in:
        st.header(f"Willkommen {st.session_state.username}!")
        st.write("Sie haben nun Zugriff auf die App. Wählen Sie eine Option links im Menü aus.")
    else:
        st.stop()  # Stoppt die weitere Ausführung der Seite, wenn nicht eingeloggt