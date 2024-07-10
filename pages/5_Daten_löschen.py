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
st.title("Person und zugehörige EKG-Daten löschen")
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
        Person.delete_person(person_id)
        st.success(f"Person {selected_person} und alle zugehörigen EKG-Tests wurden gelöscht.")

# Auswahl der zu löschenden EKG-Tests
st.title("EKG-Daten löschen")
st.session_state.selected_person = st.selectbox(
    "Wählen Sie eine Person aus",
    options=person_names_list,
    key="person_of_delete_ekg"
)

# Finden der Person - den String haben wir im Session state
current_person = Person.find_person_id_by_name(st.session_state.selected_person)
current_person_obj = Person(current_person) # Erstellen eines Person-Objekts aus dem Dictionary
person_ekg_list = EKGdata.get_ekgids_by_personid(current_person_obj.id) # Erstellen einer Liste von EKGs der gewählten Person

selected_ekg = st.selectbox(
    "Wählen Sie einen EKG-Test zum Löschen aus",
    options=person_ekg_list,
    key="delete_ekg"
)

#if selected_ekg:
 #   ekg_data = EKGdata.find_person_data_by_name(selected_person)
  #  ekg_id = int(EKGdata.find_person_id_by_name(selected_person))

if st.button("EKG-Test löschen"):
# Löschen der Person und der zugehörigen EKG-Tests
    EKGdata.delete_ekg_file(person_id)
    st.success(f"EKG-Test {selected_ekg} wurde gelöscht.")
