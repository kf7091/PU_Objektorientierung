import streamlit as st
from person import Person
from PIL import Image
from tinydb import TinyDB
from person import Person
from ekgdata import EKGdata
import os
import uuid

'''Funktioniert leider nicht. Haben bis zum Schluss versucht EKG-Daten hochzuladen konnten aber nicht die
gespeicherten Daten sinnvoll mit den Personen verknüpfen. Zum Schluss haben wir ein wenig den Copilot
arbeiten lassen aber auch das hat nicht geholfen. Wir haben uns dann entschieden die Funktion nicht zu implementieren.'''

# Überprüfung, ob der Benutzer eingeloggt ist
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Bitte loggen Sie sich zuerst ein!")
    st.stop()

person_names_list = Person.get_persons_list(TinyDB(os.path.join("data", "person_db.json")).table("persons"))

st.title("EKG-Daten hinzufügen")
if 'current_user' not in st.session_state:
    st.session_state.selected_person = 'None'

st.session_state.selected_person = st.selectbox(
    'Versuchsperson',
    options=person_names_list, key="sbVersuchsperson")

person_id = Person.find_person_id_by_name(st.session_state.selected_person)
path = os.path.join("data", "person_pictures", '{}.jpg'.format(person_id))
# File upload
uploaded_file = st.file_uploader("Datei auswählen", accept_multiple_files=False, type=".txt")

def new_func(person_id, uploaded_file):
    if uploaded_file is not None:
        # Generate unique id for the uploaded file
        file_id = str(uuid.uuid4())

        # Save file with the generated id
        file_path = os.path.join("data", "ekg_data", '{}.txt'.format(file_id))
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        # Update person_db.json with the file id and result link
        db = TinyDB(os.path.join("data", "person_db.json"))
        table = db.table("persons")
        person = table.get(doc_id=person_id)
        if 'ekg_files' not in person:
            person['ekg_files'] = []
        person['ekg_files'].append(file_id)
        result_link = os.path.join("data", "ekg_data", '{}.txt'.format(file_id))
        person['result_link'] = result_link
        table.update(person, doc_ids=[person_id])

        # Add the file to ekg_tests with a new ID
        ekg_tests_table = db.table("ekg_tests")
        ekg_test = {
            'person_id': person_id,
            'file_id': file_id,
        }
        ekg_tests_table.insert(ekg_test)

        st.success("Datei erfolgreich hochgeladen und gespeichert!")
    else:
        st.info("Bitte wählen Sie eine Datei aus.")

new_func(person_id, uploaded_file)
