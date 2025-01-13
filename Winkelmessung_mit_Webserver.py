import machine
import network
import socket
import time
from machine import I2C
from imu import MPU6050
import json
import math

# LED und Button Konfiguration
green_led = machine.Pin(25, machine.Pin.OUT)
red_led = machine.Pin(27, machine.Pin.OUT)
button = machine.Pin(26, machine.Pin.IN)
poti = machine.ADC(machine.Pin(34))
poti.atten(machine.ADC.ATTN_0DB)

# MPU6050 Sensoren initialisieren
i2c = I2C(1, scl=machine.Pin(22), sda=machine.Pin(21))
sensor_1 = MPU6050(i2c, address=0x68)
sensor_2 = MPU6050(i2c, address=0x69)

def init_sensors():
    """Initialisiert und kalibriert die Sensoren."""
    try:
        with open("calibration.json", "r") as f:
            calibration_data = json.load(f)
        
        sensor_1_offsets = calibration_data["sensor_1"]
        sensor_2_offsets = calibration_data["sensor_2"]
        
        sensor_1.x_offset = sensor_1_offsets["x_offset"]
        sensor_1.y_offset = sensor_1_offsets["y_offset"]
        sensor_1.z_offset = sensor_1_offsets["z_offset"]
        
        sensor_2.x_offset = sensor_2_offsets["x_offset"]
        sensor_2.y_offset = sensor_2_offsets["y_offset"]
        sensor_2.z_offset = sensor_2_offsets["z_offset"]
        print("Kalibrierungsdaten erfolgreich geladen")
        return True
    except Exception as e:
        print("Fehler beim Laden der Kalibrierungsdaten:", e)
        return False

def calculate_angle():
    """Berechnet den Winkel zwischen den beiden MPU6050 Sensoren."""
    try:
        acc1 = sensor_1.read_accel()
        acc2 = sensor_2.read_accel()
        
        def normalize(vector):
            magnitude = math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)
            return [v / magnitude for v in vector]
        
        v1 = normalize([acc1[0], acc1[1], acc1[2]])
        v2 = normalize([acc2[0], acc2[1], acc2[2]])
        
        dot_product = sum(v1[i] * v2[i] for i in range(3))
        angle_rad = math.acos(max(min(dot_product, 1.0), -1.0))
        return math.degrees(angle_rad)
    except Exception as e:
        print("Fehler bei der Winkelmessung:", e)
        return 0.0

def connect_wifi():
    """Verbindet mit dem WLAN."""
    ssid = "FRITZ!Box 7490"
    password = "73731537040695638431"
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print('Verbinde mit WLAN...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep(0.1)
    print('Verbunden:', wlan.ifconfig())
    return wlan.ifconfig()[0]

def setup_server():
    """Erstellt und konfiguriert den Server-Socket."""
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Versuche mehrmals den Port zu binden
    for _ in range(3):
        try:
            addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
            s.bind(addr)
            s.listen(1)
            return s
        except OSError as e:
            print(f"Versuche Socket zu erstellen... ({e})")
            try:
                s.close()
            except:
                pass
            time.sleep(2)
            s = socket.socket()
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    raise OSError("Konnte Server nicht starten")

def serve(s):
    """Hauptserver-Schleife."""
    print('Webserver läuft auf', ip)
    
    while True:
        try:
            cl, addr = s.accept()
            request = cl.recv(1024).decode('utf-8')
            
            if "/?green=on" in request:
                green_led.value(1)
            elif "/?green=off" in request:
                green_led.value(0)
            elif "/?red=on" in request:
                red_led.value(1)
            elif "/?red=off" in request:
                red_led.value(0)

            knee_angle = calculate_angle()
            poti_value = poti.read()
            button_status = "Gedrückt" if button.value() == 0 else "Nicht gedrückt"

            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta http-equiv="refresh" content="1">
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        text-align: center;
                        background-color: #f4f4f4;
                        color: #333;
                    }}
                    h1 {{
                        color: #333;
                    }}
                    .measurement {{
                        margin: 20px;
                        padding: 15px;
                        background-color: white;
                        border-radius: 8px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }}
                    .angle {{
                        font-size: 24px;
                        color: #007BFF;
                        font-weight: bold;
                    }}
                    button {{
                        padding: 15px 30px;
                        font-size: 16px;
                        margin: 10px;
                        border: none;
                        cursor: pointer;
                        border-radius: 5px;
                    }}
                    .green {{
                        background-color: #4CAF50;
                        color: white;
                    }}
                    .red {{
                        background-color: #f44336;
                        color: white;
                    }}
                </style>
            </head>
            <body>
                <h1>ESP32 Messstation</h1>
                
                <div class="measurement">
                    <h2>Kniewinkel</h2>
                    <div class="angle">{knee_angle:.1f}°</div>
                </div>
                
                <div class="measurement">
                    <p>Button-Status: <strong>{button_status}</strong></p>
                    <p>Poti-Wert: <strong>{poti_value}</strong> (0-1023)</p>
                </div>

                <form action="/" method="get">
                    <button class="green" name="green" value="on">Grüne LED An</button>
                    <button class="green" name="green" value="off">Grüne LED Aus</button>
                    <br>
                    <button class="red" name="red" value="on">Rote LED An</button>
                    <button class="red" name="red" value="off">Rote LED Aus</button>
                </form>
            </body>
            </html>
            """

            cl.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n")
            cl.send(html)
            cl.close()

        except Exception as e:
            print("Fehler in Server-Schleife:", e)
            try:
                cl.close()
            except:
                pass

# Hauptprogramm
print("Starte ESP32 Webserver...")
if not init_sensors():
    print("Fehler bei der Sensor-Initialisierung")
    raise SystemExit

ip = connect_wifi()
green_led.value(0)
red_led.value(0)

try:
    server_socket = setup_server()
    serve(server_socket)
except Exception as e:
    print("Kritischer Fehler:", e)
    try:
        server_socket.close()
    except:
        pass
