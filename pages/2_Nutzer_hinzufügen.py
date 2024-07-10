import streamlit as st
from person import Person
from PIL import Image

# Überprüft ob Nutzer eingeloggt ist
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Bitte loggen Sie sich zuerst auf der Startseite ein oder erstellen Sie einen neuen Benutzer!")
    st.stop()

st.title("Personen hinzufügen")

# Formular für die neue Person
firstname = st.text_input("Vorname")
lastname = st.text_input("Nachname")
year_of_birth = st.number_input("Geburtsjahr", min_value=1850, max_value=2024, step=1)
picture_path = st.text_input("Pfad zum Bild")

# Button zum Hinzufügen der Person
if st.button("Person hinzufügen"):
    if firstname and lastname and year_of_birth and picture_path:
        Person.add_person(firstname, lastname, year_of_birth, picture_path)
        st.success(f"Person {firstname} {lastname} hinzugefügt")
    elif firstname and lastname and year_of_birth:
        picture_path = "data/pictures/empty.png"
        Person.add_person(firstname, lastname, year_of_birth, picture_path)
        st.success(f"Person {firstname} {lastname} hinzugefügt")
    else:
        st.error("Bitte geben Sie einen Vornamen, Nachnamen und das Geburtsjahr ein!")

uploaded_picture = st.file_uploader("Bild hochladen", type=["png", "jpg", "jpeg"], accept_multiple_files=False, key="uploaded_picture")
