import streamlit as st
from person import Person
from PIL import Image

person_data = Person.load_person_data() 
person_names_list = Person.get_person_list(person_data)

# Session State wird leer angelegt, solange er noch nicht existiert
if 'current_user' not in st.session_state:
    st.session_state.current_user = 'None'

st.write("# EKG APP") # Eine Überschrift der ersten Ebene
st.write("## Versuchsperson auswählen") # Eine Überschrift der zweiten Ebene

# Dieses Mal speichern wir die Auswahl als Session State
st.session_state.current_user = st.selectbox(
    'Versuchsperson',
    options = person_names_list, key="sbVersuchsperson")

# Finden der Person - den String haben wir im Session state
current_person = Person.find_person_data_by_name(st.session_state.current_user)

"""picture_path ist ein Key im Dictionary, der den Pfad zum Bild enthält"""
image = Image.open(current_person["picture_path"]) # Bild laden und # Auslesen des Pfades aus dem zurückgegebenen Dictionary

st.image(image, caption = st.session_state.current_user) # Bild anzeigen lassen

st.write("Name der ausgewählten Versuchsperson: ", st.session_state.current_user) 


'''Drop down mit ID / Datum um EKG Daten zu laden und anzuzeigen
   wieder eine Liste erstellen der EKGs wie bei den Personen mit Vorname und Nachname
   '''