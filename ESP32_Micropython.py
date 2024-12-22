import time
import network
import socket
import bno055
from machine import Pin, I2C

# Setup für das BNO055 IMU-Modul
i2c = I2C(scl=Pin(22), sda=Pin(21))  # Hier Pin-Nummern anpassen
imu = bno055.BNO055(i2c)

# WLAN-Verbindung herstellen
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect('dein_wlan_name', 'dein_wlan_passwort')
    while not wlan.isconnected():
        time.sleep(0.5)
    print('WLAN verbunden', wlan.ifconfig())

# Starten der WLAN-Verbindung
connect_wifi()

# Erstellen eines Sockets für die Kommunikation mit Streamlit
def create_socket():
    addr = socket.getaddrinfo('0.0.0.0', 8080)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('Listening on', addr)
    return s

# Funktion zum Senden der IMU-Daten
def send_imu_data(client_socket):
    while True:
        # Hole die Euler-Winkel (Roll, Pitch, Yaw)
        euler_angles = imu.read_euler()
        data = f"{euler_angles[0]},{euler_angles[1]},{euler_angles[2]}"
        client_socket.send(data.encode('utf-8'))
        time.sleep(0.1)

# Hauptfunktion
def main():
    s = create_socket()
    while True:
        client_socket, client_addr = s.accept()
        print('Client verbunden:', client_addr)
        send_imu_data(client_socket)

if __name__ == '__main__':
    main()
