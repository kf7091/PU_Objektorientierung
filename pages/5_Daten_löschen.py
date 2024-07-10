import streamlit as st
from person import Person
from ekgdata import EKGdata

# Überprüfung, ob der Benutzer eingeloggt ist
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Bitte loggen Sie sich zuerst ein!")
    st.stop()

# Laden der Personendaten
person_data = Person.load_person_data()
person_names_list = Person.get_persons_list(person_data)

# Auswahl der zu löschenden Person
st.title("Personen- und EKG-Daten löschen")
selected_person = st.selectbox(
    "Wählen Sie eine Person zum Löschen aus",
    options=person_names_list,
    key="delete_person"
)

if selected_person:
    person_data = Person.find_person_data_by_name(selected_person)
    person_id = int(Person.find_person_id_by_name(selected_person))

    if st.button("Person und zugehörige EKG-Tests löschen"):
        # Löschen der Person und der zugehörigen EKG-Tests
        person.delete_person(person_id)
        st.success(f"Person {selected_person} und alle zugehörigen EKG-Tests wurden gelöscht.")