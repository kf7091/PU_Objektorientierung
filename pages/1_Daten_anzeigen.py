import streamlit as st
from person import Person
from PIL import Image
from ekgdata import EKGdata
import plotly.graph_objects as go
from tinydb import TinyDB

st.set_page_config(page_title="Personen- and EKG-Daten", page_icon="📈")

# Überprüft ob Nutzer eingeloggt ist
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Bitte loggen Sie sich zuerst auf der Startseite ein oder erstellen Sie einen neuen Benutzer!")
    st.stop()

st.title("Personen- und EKG-Daten")

person_data = Person.load_person_data()
db = TinyDB("data/person_db.json")
person_names_list = Person.get_persons_list(db.table("persons"))


# Session State wird leer angelegt, solange er noch nicht existiert
if 'current_user' not in st.session_state:
    st.session_state.current_user = 'None'
    st.session_state.selected_person = 'None'
    st.session_state.selected_ekg = 'None' 

st.write("### Versuchsperson auswählen") # Eine Überschrift der zweiten Ebene

st.session_state.selected_person = st.selectbox(
    'Versuchsperson',
    options = person_names_list, key="sbVersuchsperson")

# Finden der Person - den String haben wir im Session state
current_person = Person.find_person_id_by_name(st.session_state.selected_person)
current_person_obj = Person(current_person) # Erstellen eines Person-Objekts aus dem Dictionary
person_ekg_list = EKGdata.get_ekgids_by_personid(current_person_obj.id) # Erstellen einer Liste von EKGs der gewählten Person

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

st.write("Ausgewähltes EKG: ", st.session_state.current_user, "von:", current_person_obj.firstname, current_person_obj.lastname)

try:
    ekg = EKGdata(st.session_state.current_user)
    ekg.find_peaks(threshold=340, respacing_factor=4)
    hr = ekg.estimate_hr()
    hr_warning = ekg.max_hr_warning(current_person_obj.max_hr_bpm)
except:
    st.write("Keine Daten vorhanden. Andere Person wählen!")

# Tab-Elemente erstellen
tab1, tab2 = st.tabs(["Daten", "Grafik"])


#st.image(image, caption = st.session_state.current_user) # Bild anzeigen lassen --> wurde ersetzt
#st.write("Name der ausgewählten Versuchsperson: ", st.session_state.current_user) --> wurde erstezt 

try:
    with tab1:
        if ekg.hr_warning:
            st.warning("Die maximale Herzfrequenz wurde zu lange überschritten!")
        if not ekg.ekg_valid():
            st.error("EKG Daten sind ungültig!")
        st.write("Daten des EKGs: {}".format(st.session_state.current_user))
        st.write('Datum:', ekg.date)
        st.write("Durchschnittliche Herzfrequenz: ", int(hr.mean()))

    with tab2:
        if ekg.hr_warning:
            st.warning("Die maximale Herzfrequenz wurde zu lange überschritten!")
        if not ekg.ekg_valid():
            st.error("EKG Daten sind ungültig!")
        st.write('Länge des EKGs in sekunden:', ekg.legnth/1000)
        ekg.plot_hr_series()
        st.plotly_chart(ekg.hr_plot, use_container_width=True)
except:
    st.write("Keine Daten vorhanden. Andere Person wählen!")

    
    