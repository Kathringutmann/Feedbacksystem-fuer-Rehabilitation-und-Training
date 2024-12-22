import streamlit as st
import socket
import time

# Funktion zur Verbindung mit dem ESP32-Server
def connect_to_esp32():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('IP_DES_ESP32', 8080))  # IP-Adresse des ESP32 anpassen
    return s

# Streamlit-App zur Anzeige der IMU-Daten
def display_imu_data():
    st.title("IMU-Daten Visualisierung")
    
    # Verbinde zur ESP32
    s = connect_to_esp32()
    
    st.subheader("Echtzeit-Daten:")
    
    # Initialisiere Werte
    roll = pitch = yaw = 0.0
    
    try:
        while True:
            data = s.recv(1024).decode('utf-8')
            if data:
                roll, pitch, yaw = map(float, data.split(','))
                st.write(f"Roll: {roll:.2f}°  |  Pitch: {pitch:.2f}°  |  Yaw: {yaw:.2f}°")
                time.sleep(0.1)
            else:
                st.write("Verbindung unterbrochen.")
                break
    except KeyboardInterrupt:
        st.write("Verbindung beendet.")
    finally:
        s.close()

# Hauptfunktion zum Starten der App
if __name__ == '__main__':
    display_imu_data()
