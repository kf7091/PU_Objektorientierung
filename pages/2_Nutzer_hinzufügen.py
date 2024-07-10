import streamlit as st
from person import Person
from PIL import Image
from tinydb import TinyDB
from person import Person
import os

# Überprüft ob Nutzer eingeloggt ist
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Bitte loggen Sie sich zuerst auf der Startseite ein oder erstellen Sie einen neuen Benutzer!")
    st.stop()

tab1, tab2 = st.tabs(["Personen hinzufügen", "Bild hochladen"])
with tab1:
    st.title("Personen hinzufügen")

    # Formular für die neue Person
    firstname = st.text_input("Vorname")
    lastname = st.text_input("Nachname")
    year_of_birth = st.number_input("Geburtsjahr", min_value=1850, max_value=2024, step=1)
    #picture_path = st.text_input("Pfad zum Bild")

    # Button zum Hinzufügen der Person
    if st.button("Person hinzufügen"):
        if firstname and lastname and year_of_birth:
            picture_path = "data/pictures/empty.png"
            Person.add_person(firstname, lastname, year_of_birth, picture_path)
            st.success(f"Person {firstname} {lastname} hinzugefügt")
        else:
            st.error("Bitte geben Sie einen Vornamen, Nachnamen und das Geburtsjahr ein!")
with tab2:

    person_names_list = Person.get_persons_list(TinyDB("data/person_db.json").table("persons"))

    if 'current_user' not in st.session_state:
        st.session_state.selected_person = 'None'

    st.session_state.selected_person = st.selectbox(
        'Versuchsperson',
        options = person_names_list, key="sbVersuchsperson")

    person_id = Person.find_person_id_by_name(st.session_state.selected_person)
    path = "data" + os.sep + "person_pictures" + os.sep + '{}.jpg'.format(person_id)
    
    #uploaded_picture = st.file_uploader("Bild hochladen", type=["png", "jpg", "jpeg"], accept_multiple_files=False, key="uploaded_picture")
    uploaded_picture = st.file_uploader("Bild hochladen", type="jpg", accept_multiple_files=False, key="uploaded_picture")
    if st.button("Bild hochladen"):
        if uploaded_picture is not None:
            #path = os.path.join("data", "person_pictures", '{}.jpg'.format(person_id))
            
            image = Image.open(uploaded_picture)
            image.save(path)
            st.success("Bild erfolgreich hochgeladen!")
    if st.button("Bild löschen"):
        path = path
        os.remove(path)
        st.success("Bild erfolgreich gelöscht!")

    try:
        image = Image.open(path)
        st.image(image, width=140)
    except:
        image = Image.open("data" + os.sep + "person_pictures" + os.sep + "empty.png")
        st.image("data" + os.sep + "person_pictures" + os.sep + "empty.png", width=140)
