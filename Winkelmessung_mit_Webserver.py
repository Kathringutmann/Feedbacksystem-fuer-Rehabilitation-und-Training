import machine              # Importiere das 'machine'-Modul, das Hardware-Funktionen wie Pins und ADC unterstützt
import network             # Importiere das 'network'-Modul für WLAN-Verbindungen
import socket              # Importiere das 'socket'-Modul für Netzwerkkommunikation
import time                # Importiere das 'time'-Modul für Zeitfunktionen
from machine import I2C    # Importiere das I2C-Modul aus 'machine' zum Kommunizieren mit I2C-Geräten
from imu import MPU6050    # Importiere die MPU6050-Bibliothek für den Zugriff auf den Sensor
import json                # Importiere das 'json'-Modul für das Arbeiten mit JSON-Daten
import math                # Importiere das 'math'-Modul für mathematische Berechnungen
from html_template import generate_html  # Importiere eine Funktion zur HTML-Generierung

# MPU6050 Sensoren initialisieren
i2c = I2C(1, scl=machine.Pin(22), sda=machine.Pin(21))  # Initialisiere I2C mit Pin 22 als SCL und Pin 21 als SDA
sensor_1 = MPU6050(i2c, address=0x68)  # Initialisiere den ersten MPU6050-Sensor mit der Adresse 0x68
sensor_2 = MPU6050(i2c, address=0x69)  # Initialisiere den zweiten MPU6050-Sensor mit der Adresse 0x69

def init_sensors():
    """Initialisiert und kalibriert die Sensoren."""
    try:
        # Versuche, Kalibrierungsdaten aus einer Datei zu laden
        with open("calibration.json", "r") as f:
            calibration_data = json.load(f)  # Lese die Kalibrierungsdaten aus der JSON-Datei
        
        # Setze die Kalibrierungs-Offsets für Sensor 1
        sensor_1_offsets = calibration_data["sensor_1"]
        sensor_1.x_offset = sensor_1_offsets["x_offset"]
        sensor_1.y_offset = sensor_1_offsets["y_offset"]
        sensor_1.z_offset = sensor_1_offsets["z_offset"]
        
        # Setze die Kalibrierungs-Offsets für Sensor 2
        sensor_2_offsets = calibration_data["sensor_2"]
        sensor_2.x_offset = sensor_2_offsets["x_offset"]
        sensor_2.y_offset = sensor_2_offsets["y_offset"]
        sensor_2.z_offset = sensor_2_offsets["z_offset"]
        
        print("Kalibrierungsdaten erfolgreich geladen")
        return True  # Rückgabewert True, wenn die Initialisierung erfolgreich war
    except Exception as e:
        print("Fehler beim Laden der Kalibrierungsdaten:", e)
        return False  # Rückgabewert False, wenn es einen Fehler gab

def calculate_angle():
    """Berechnet den Winkel zwischen den beiden MPU6050 Sensoren."""
    try:
        # Lese die Beschleunigungsdaten der beiden Sensoren
        acc1 = sensor_1.read_accel()
        acc2 = sensor_2.read_accel()
        
        # Normiere die Beschleunigungsvektoren
        def normalize(vector):
            # Berechne die Magnitude des Vektors
            magnitude = math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)
            # Normiere den Vektor, indem jeder Wert durch die Magnitude geteilt wird
            return [v / magnitude for v in vector]
        
        # Normalisiere die Beschleunigungsvektoren der beiden Sensoren
        v1 = normalize([acc1[0], acc1[1], acc1[2]])
        v2 = normalize([acc2[0], acc2[1], acc2[2]])
        
        # Berechne das Skalarprodukt der beiden normalisierten Vektoren
        dot_product = sum(v1[i] * v2[i] for i in range(3))
        
        # Berechne den Winkel in Bogenmaß zwischen den beiden Vektoren
        angle_rad = math.acos(max(min(dot_product, 1.0), -1.0))
        
        # Gib den Winkel in Grad zurück
        return math.degrees(angle_rad)
    except Exception as e:
        print("Fehler bei der Winkelmessung:", e)
        return 0.0  # Falls ein Fehler auftritt, gib 0 zurück

def connect_wifi():
    """Verbindet mit dem WLAN."""
    ssid = "FRITZ!Box 7490"  # SSID des WLANs
    password = "73731537040695638431"  # Passwort des WLANs
    wlan = network.WLAN(network.STA_IF)  # Erstelle ein WLAN-Objekt im Station-Modus
    wlan.active(True)  # Aktiviere das WLAN-Modul
    
    if not wlan.isconnected():  # Wenn nicht mit dem WLAN verbunden
        print('Verbinde mit WLAN...')
        wlan.connect(ssid, password)  # Versuche, eine Verbindung mit dem WLAN herzustellen
        while not wlan.isconnected():  # Solange keine Verbindung besteht, warte
            time.sleep(0.1)
    print('Verbunden:', wlan.ifconfig())  # Gib die IP-Adresse des ESP32 aus
    return wlan.ifconfig()[0]  # Gib die IP-Adresse des ESP32 zurück

def setup_server():
    """Erstellt und konfiguriert den Server-Socket."""
    s = socket.socket()  # Erstelle einen neuen Socket
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Erlaube das Wiederverwenden von Adressen
    
    for _ in range(3):  # Versuche bis zu 3 Mal, den Server zu starten
        try:
            addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]  # Hole die IP-Adresse für den Server
            s.bind(addr)  # Binde den Socket an die Adresse
            s.listen(1)  # Setze den Socket in den Listen-Modus
            return s  # Gib den Server-Socket zurück
        except OSError as e:
            print(f"Versuche Socket zu erstellen... ({e})")
            try:
                s.close()  # Schließe den Socket, falls ein Fehler auftritt
            except:
                pass
            time.sleep(2)  # Warte 2 Sekunden und versuche es erneut
            s = socket.socket()  # Erstelle einen neuen Socket
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Erlaube das Wiederverwenden von Adressen
    
    raise OSError("Konnte Server nicht starten")  # Wenn es 3 Versuche lang fehlschlägt, gebe einen Fehler aus

def serve(s):
    """Hauptserver-Schleife."""
    print('Webserver läuft auf', ip)  # Zeige die IP-Adresse des Servers an
    
    while True:  # Endlosschleife für den Serverbetrieb
        try:
            cl, addr = s.accept()  # Warte auf einen Client und akzeptiere die Verbindung
            request = cl.recv(1024).decode('utf-8')  # Lese die Anfrage des Clients
            
            # Berechne den aktuellen Winkel zwischen den beiden MPU6050-Sensoren
            knee_angle = calculate_angle()
            
            # Generiere HTML mit dem aktuellen Winkel
            html = generate_html(knee_angle)
            
            # Sende die HTML-Antwort an den Client
            cl.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n")
            cl.send(html)  # Sende das HTML
            cl.close()  # Schließe die Verbindung
        except Exception as e:
            print("Fehler in Server-Schleife:", e)
            try:
                cl.close()  # Versuche, die Client-Verbindung zu schließen
            except:
                pass

# Hauptprogramm
print("Starte ESP32 Webserver...")  # Gib aus, dass der Webserver gestartet wird
if not init_sensors():  # Initialisiere die Sensoren, wenn es fehlschlägt, beende das Programm
    print("Fehler bei der Sensor-Initialisierung")
    raise SystemExit

ip = connect_wifi()  # Stelle eine WLAN-Verbindung her und hole die IP-Adresse

try:
    server_socket = setup_server()  # Richte den Server ein
    serve(server_socket)  # Starte die Server-Schleife
except Exception as e:
    print("Kritischer Fehler:", e)  # Falls ein Fehler auftritt, gebe eine Fehlermeldung aus
    try:
        server_socket.close()  # Versuche, den Server-Socket zu schließen
    except:
        pass

