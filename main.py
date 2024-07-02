import streamlit as st
from person import Person
from PIL import Image
from ekgdata import EKGdata
import plotly.graph_objects as go
from tinydb import TinyDB

person_data = Person.load_person_data()
db = TinyDB("data/person_db.json")
person_names_list = Person.get_persons_list(db.table("persons"))


# Session State wird leer angelegt, solange er noch nicht existiert
if 'current_user' not in st.session_state:
    st.session_state.current_user = 'None'
    st.session_state.selected_person = 'None'
    st.session_state.selected_ekg = 'None'

st.write("# EKG APP") # Eine Überschrift der ersten Ebene
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
    ekg.find_peaks(340, 4)
    hr = ekg.estimate_hr()
except:
    st.write("Keine Daten vorhanden. Andere Person wählen!")

# Tab-Elemente erstellen
tab1, tab2 = st.tabs(["Daten", "Grafik"])


#st.image(image, caption = st.session_state.current_user) # Bild anzeigen lassen --> wurde ersetzt
#st.write("Name der ausgewählten Versuchsperson: ", st.session_state.current_user) --> wurde erstezt 

try:
    with tab1:
        st.write("Daten des EKGs: {}".format(st.session_state.current_user))
        st.write('Datum:', ekg.date)
        st.write("Durchschnittliche Herzfrequenz: ", int(hr.mean()))

    with tab2:
        fig = go.Figure(data=go.Scatter(x=hr.index/1000, y=hr), layout=go.Layout(title="Herzfrequenz" ,xaxis_title="Zeit in s", yaxis_title="Herzfrequenz in bpm"))
        fig.update_layout(
            xaxis=dict(
                rangeslider=dict(
                    visible=True
                ),
                type="linear"
            )
        )
        st.plotly_chart(fig, use_container_width=True)
except:
    st.write("Keine Daten vorhanden. Andere Person wählen!")
    