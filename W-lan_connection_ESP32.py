import network
import socket
import time

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect('FRITZ!Box 6660 Cable LI', '52777539319005712732')
    while not wlan.isconnected():
        time.sleep(0.5)
    print('WLAN verbunden', wlan.ifconfig())  # IP-Adresse des ESP32 hier auslesen


# TCP/IP-Server starten
def start_server():
    addr = socket.getaddrinfo('0.0.0.0', 8080)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('Server gestartet auf', addr)
    return s

# Empfangen der IMU-Daten
def receive_imu_data(client_socket):
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if data:
            print("Empfangene IMU-Daten:", data)
        time.sleep(0.1)

# Hauptfunktion
def main():
    connect_wifi()
    s = start_server()
    client_socket, client_addr = s.accept()
    print('Client verbunden:', client_addr)
    receive_imu_data(client_socket)

if __name__ == '__main__':
    main()
