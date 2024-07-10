import streamlit as st
from person import Person
from PIL import Image
from tinydb import TinyDB
from person import Person
import os

# Überprüfung, ob der Benutzer eingeloggt ist
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Bitte loggen Sie sich zuerst ein!")
    st.stop()

st.title("EKG-Daten hinzufügen")

# File upload
uploaded_file = st.file_uploader("Datei auswählen", accept_multiple_files=False, type=".txt")

if uploaded_file is not None:
    # Save file
    file_path = os.path.join("data", "ekg_data", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())
    st.success("Datei erfolgreich hochgeladen und gespeichert!")
else:
    st.info("Bitte wählen Sie eine Datei aus.")
