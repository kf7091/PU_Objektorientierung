import streamlit as st

st.title("Personen hinzufügen")
id = 1
uploaded_picture = st.file_uploader("Bild hochladen", type="jpg", accept_multiple_files=False, key="uploaded_picture")
folder = "data/pictures/"
path = folder + '{}.jpg'.format(id)
with open(path, "wb") as file:
    file.write(uploaded_picture.read())
    file.close()