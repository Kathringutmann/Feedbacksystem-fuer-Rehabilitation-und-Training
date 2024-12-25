import streamlit as st
from PIL import Image

# Hauptmenü-Funktion
def main_menu():
    st.title("Feedbacksystem für Rehabilitation und Training")
    st.subheader("Bitte wählen Sie ein Gelenk aus:")

    # Erstelle Layout-Spalten für das Bild und den Button, die beide nebeneinander sind
    col1, col2 = st.columns([1, 1])  # Bild nimmt mehr Platz als der Button

    with col1:
        # Anzeige des Bildes für das Kniegelenk
        st.write("**Kniegelenk**")
        knie_image = Image.open("kniegelenk_128570975.jpg")
        knie_image = knie_image.resize((200, 200))  # Bildgröße anpassen
        st.image(knie_image, width=200, use_container_width=False)

    with col2:
        # Button zum Menü mit der Winkelmessung, auf der Höhe des Bildes
        if st.button("Winkelmessung Kniegelenk", key="knie_button", help="Zum Kniegelenk (Klick auf den Button)"):
            knie_menu()

    # Weitere Gelenke: Schulter und Hüfte
    col1, col2 = st.columns([1, 1])  # Spalten für Schultergelenk und Button
    with col1:
        # Anzeige des Bildes für das Schultergelenk
        st.write("**Schultergelenk**")
        shoulder_image = Image.open("shoulder-1-600x600.jpg")
        shoulder_image = shoulder_image.resize((200, 200))  # Bildgröße anpassen
        st.image(shoulder_image, width=200, use_container_width=False)

    with col2:
        # Button für Schultergelenk
        if st.button("Winkelmessung Schultergelenk", key="shoulder_button", help="Zum Schultergelenk (Klick auf den Button)"):
            shoulder_menu()

    col1, col2 = st.columns([1, 1])  # Spalten für Hüftgelenk und Button
    with col1:
        # Anzeige des Bildes für das Hüftgelenk
        st.write("**Hüftgelenk**")
        hip_image = Image.open("shutterstock_485980747-960x720.jpg")  # Beispielbild für Hüfte
        hip_image = hip_image.resize((200, 200))  # Bildgröße anpassen
        st.image(hip_image, width=200, use_container_width=False)

    with col2:
        # Button für Hüftgelenk
        if st.button("Winkelmessung Hüftgelenk", key="hip_button", help="Zum Hüftgelenk (Klick auf den Button)"):
            hip_menu()

# Knie-Menü-Funktion (mit Sensor-Daten)
def knie_menu():
    st.title("Kniegelenk Winkelmessung")
    st.write("Aktuelle Winkelmessung:")

    # Beispiel für einen Winkelwert, hier als 45
    angle = 45  # Dies könnte später durch echte Sensordaten ersetzt werden
    
    # Zeige die Zahl als große Zahl
    st.markdown(f"<h1 style='text-align: center; font-size: 180px;'>{angle}°</h1>", unsafe_allow_html=True)

    if st.button("Zurück zum Hauptmenü"):
        main_menu()

# Schulter-Menü-Funktion (mit Platzhalter für Sensor-Daten)
def shoulder_menu():
    st.title("Schultergelenk Winkelmessung")
    st.write("Aktuelle Winkelmessung:")

    # Beispiel für einen Winkelwert, hier als 60
    angle = 60  # Dies könnte später durch echte Sensordaten ersetzt werden
    
    # Zeige die Zahl als große Zahl
    st.markdown(f"<h1 style='text-align: center; font-size: 180px;'>{angle}°</h1>", unsafe_allow_html=True)

    if st.button("Zurück zum Hauptmenü"):
        main_menu()

# Hüft-Menü-Funktion (mit Platzhalter für Sensor-Daten)
def hip_menu():
    st.title("Hüftgelenk Winkelmessung")
    st.write("Aktuelle Winkelmessung:")

    # Beispiel für einen Winkelwert, hier als 90
    angle = 90  # Dies könnte später durch echte Sensordaten ersetzt werden
    
    # Zeige die Zahl als große Zahl
    st.markdown(f"<h1 style='text-align: center; font-size: 180px;'>{angle}°</h1>", unsafe_allow_html=True)

    if st.button("Zurück zum Hauptmenü"):
        main_menu()

# Starte die App mit dem Hauptmenü
if __name__ == "__main__":
    main_menu()
