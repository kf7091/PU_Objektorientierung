import streamlit as st
from person import Person
from PIL import Image

person_data = Person.load_person_data() 
person_names_list = Person.get_person_list(person_data)


# Session State wird leer angelegt, solange er noch nicht existiert
if 'current_user' not in st.session_state:
    st.session_state.current_user = 'None'

st.write("# EKG APP") # Eine Überschrift der ersten Ebene
st.write("### Versuchsperson auswählen") # Eine Überschrift der zweiten Ebene

st.session_state.current_user = st.selectbox(
    'Versuchsperson',
    options = person_names_list, key="sbVersuchsperson")

# Finden der Person - den String haben wir im Session state
current_person = Person.find_person_data_by_name(st.session_state.current_user)
current_person_obj = Person(current_person) # Erstellen eines Person-Objekts aus dem Dictionary
person_ekg_list = Person.ekgs_of_person(person_data, current_person_obj.id) # Erstellen einer Liste von EKGs der gewählten Person

image = Image.open(current_person_obj.picture_path) # Bild laden und Auslesen des Pfades aus dem zurückgegebenen Dictionary

# Bild und Informationen nebeneinander anzeigen
left, col1, mid, col2 = st.columns([10,1,10,20])
with col1:
    st.image(image, width=140)
with col2:
    st.write('**Vorname:**', current_person_obj.firstname)
    st.write('**Nachname:**', current_person_obj.lastname)
    st.write('**Alter:**', current_person_obj.age)
    st.write('**Max HR:**', current_person_obj.max_hr_bpm)

st.session_state.current_user = st.selectbox(
    'EKG-Daten auswählen:',
    options = person_ekg_list, key="sbEKGliste")

# Tab-Elemente erstellen
tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])


#st.image(image, caption = st.session_state.current_user) # Bild anzeigen lassen --> wurde ersetzt
#st.write("Name der ausgewählten Versuchsperson: ", st.session_state.current_user) --> wurde erstezt 


'''Drop down mit ID / Datum um EKG Daten zu laden und anzuzeigen
   wieder eine Liste erstellen der EKGs wie bei den Personen mit Vorname und Nachname
'''

