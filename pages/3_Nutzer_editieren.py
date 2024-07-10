import streamlit as st
from person import Person
from PIL import Image

# Überprüfung, ob der Benutzer eingeloggt ist
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Bitte loggen Sie sich zuerst ein!")
    st.stop()

# Laden der Personendaten
person_data = Person.load_person_data()
person_names_list = Person.get_persons_list(person_data)

# Auswahl der zu bearbeitenden Person
st.write("## Personendaten bearbeiten")
selected_person = st.selectbox(
    "Wählen Sie eine Person zum Bearbeiten aus",
    options=person_names_list,
    key="edit_person"
)

if selected_person:
    person_data = Person.find_person_data_by_name(selected_person)
    person_id = int(Person.find_person_id_by_name(selected_person))
    person_info = person_data

    # Eingabefelder für die Personendaten
    firstname = st.text_input("Vorname", value=person_info['firstname'])
    lastname = st.text_input("Nachname", value=person_info['lastname'])
    year_of_birth = st.number_input("Geburtsjahr", value=person_info['year_of_birth'], format="%d")
    picture_path = st.text_input("Bildpfad", value=person_info['picture_path'])

    if st.button("Personendaten aktualisieren"):
        # Aktualisieren der Personendaten
        Person.update_person(person_id, firstname, lastname, year_of_birth, picture_path)
        st.success(f"Personendaten für {firstname} {lastname} wurden aktualisiert.")

    # Anzeige des Bildes, wenn der Pfad angegeben ist
#    if picture_path:
#      try:
#            image = Image.open(picture_path)
#            st.image(image, caption=f"Bild von {firstname} {lastname}")
#        except Exception as e:
#            st.error(f"Bild konnte nicht geladen werden: {e}")


