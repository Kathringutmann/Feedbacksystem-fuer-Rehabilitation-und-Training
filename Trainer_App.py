import streamlit as st
import websockets  # Verwende das asynchrone websockets-Modul
import json
import asyncio
import threading

# Globale Variable für den aktuellen Winkel
current_angle = 0
is_connected = False

# Callback-Funktion für empfangene WebSocket-Nachrichten
async def on_message(websocket):
    global current_angle
    try:
        async for message in websocket:
            data = json.loads(message)  # Nachricht als JSON laden
            if "angle" in data:
                current_angle = data["angle"]
    except Exception as e:
        print(f"Fehler beim Verarbeiten der Nachricht: {e}")

# WebSocket-Verbindung herstellen
async def start_websocket():
    global is_connected
    is_connected = True
    uri = "ws://192.168.178.71:8501"  # Ersetze mit der IP deines Servers, falls erforderlich
    async with websockets.connect(uri) as websocket:
        await on_message(websocket)

# WebSocket-Thread starten
def start_websocket_thread():
    loop = asyncio.new_event_loop()  # Erstelle ein neues Event-Loop
    threading.Thread(target=lambda: loop.run_until_complete(start_websocket()), daemon=True).start()

# Hauptmenü-Funktion
def main_menu():
    st.title("Feedbacksystem für Rehabilitation und Training")
    st.subheader("Bitte wählen Sie ein Gelenk aus:")

    col1, col2 = st.columns([1, 1])  # Bild und Button in Spalten

    with col1:
        st.write("**Kniegelenk**")
        st.image("kniegelenk_128570975.jpg", width=200)

    with col2:
        if st.button("Winkelmessung Kniegelenk", key="knie_button"):
            knie_menu()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.write("**Schultergelenk**")
        st.image("shoulder-1-600x600.jpg", width=200)

    with col2:
        if st.button("Winkelmessung Schultergelenk", key="shoulder_button"):
            shoulder_menu()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.write("**Hüftgelenk**")
        st.image("shutterstock_485980747-960x720.jpg", width=200)

    with col2:
        if st.button("Winkelmessung Hüftgelenk", key="hip_button"):
            hip_menu()

# Knie-Menü-Funktion
def knie_menu():
    st.title("Kniegelenk Winkelmessung")
    st.write("Aktuelle Winkelmessung:")

    global current_angle
    angle_placeholder = st.empty()  # Platzhalter für den Winkel

    # Zeige Winkel in Echtzeit, ohne eine Schleife
    angle_placeholder.markdown(
        f"<h1 style='text-align: center; font-size: 180px;'>{current_angle:.2f}°</h1>",
        unsafe_allow_html=True
    )

    # Verwende einen einzigartigen key für den Button
    if st.button("Zurück zum Hauptmenü", key="knie_return_button_unique"):
        main_menu()

# Schulter- und Hüft-Menüs (Platzhalter)
def shoulder_menu():
    st.title("Schultergelenk Winkelmessung")
    st.write("Aktuelle Winkelmessung:")
    st.markdown("<h1 style='text-align: center; font-size: 180px;'>60°</h1>", unsafe_allow_html=True)
    if st.button("Zurück zum Hauptmenü", key="shoulder_return_button_unique"):
        main_menu()

def hip_menu():
    st.title("Hüftgelenk Winkelmessung")
    st.write("Aktuelle Winkelmessung:")
    st.markdown("<h1 style='text-align: center; font-size: 180px;'>90°</h1>", unsafe_allow_html=True)
    if st.button("Zurück zum Hauptmenü", key="hip_return_button_unique"):
        main_menu()

# Starte die App
if __name__ == "__main__":
    if not is_connected:
        start_websocket_thread()
    main_menu()
