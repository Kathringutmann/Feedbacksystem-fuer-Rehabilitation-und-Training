import uasyncio as asyncio
from machine import Pin, ADC
import network

# Verbindungsdaten deines WLANs
SSID = "DeinWLAN"
PASSWORD = "DeinPasswort"

# Globale Winkel-Daten
current_angle = {
    "knee": 45.0,  # Beispielwert für Kniegelenk
    "shoulder": 60.0,  # Beispielwert für Schultergelenk
    "hip": 90.0  # Beispielwert für Hüftgelenk
}

# Sensor (simuliert hier mit einem Potentiometer oder ADC-Eingang)
adc = ADC(Pin(36))  # Verwende einen freien ADC-Pin
adc.atten(ADC.ATTN_11DB)  # Spannungsspanne auf 3.3V erweitern

def read_sensor():
    """Simuliert die Winkelmessung."""
    raw_value = adc.read()
    return (raw_value / 4095) * 180  # Skalierung auf Winkel (0–180°)

async def update_angles():
    """Aktualisiert die Winkelwerte periodisch."""
    global current_angle
    while True:
        current_angle["knee"] = read_sensor()
        current_angle["shoulder"] = read_sensor() + 10  # Beispielabweichung
        current_angle["hip"] = read_sensor() + 20
        await asyncio.sleep(1)  # Aktualisierung alle 1 Sekunde

async def serve_client(reader, writer):
    """HTTP-Server, um die Winkel anzuzeigen."""
    try:
        request_line = await reader.readline()
        print("Request:", request_line)

        # Generiere eine einfache HTML-Seite
        response = f"""
        <html>
        <head>
            <title>Winkelmessung</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    text-align: center;
                    margin-top: 50px;
                }}
                h1 {{
                    font-size: 2em;
                    color: #333;
                }}
                .angle {{
                    font-size: 5em;
                    color: #007BFF;
                }}
                .menu {{
                    margin-top: 30px;
                }}
                .menu a {{
                    display: inline-block;
                    margin: 10px;
                    padding: 10px 20px;
                    background-color: #007BFF;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                }}
                .menu a:hover {{
                    background-color: #0056b3;
                }}
            </style>
        </head>
        <body>
            <h1>Feedbacksystem für Rehabilitation und Training</h1>
            <div>
                <h2>Kniegelenk</h2>
                <div class="angle">{current_angle['knee']:.2f}°</div>
            </div>
            <div>
                <h2>Schultergelenk</h2>
                <div class="angle">{current_angle['shoulder']:.2f}°</div>
            </div>
            <div>
                <h2>Hüftgelenk</h2>
                <div class="angle">{current_angle['hip']:.2f}°</div>
            </div>
            <div class="menu">
                <a href="/">Aktualisieren</a>
            </div>
        </body>
        </html>
        """

        # HTTP-Header
        writer.write("HTTP/1.1 200 OK\r\n")
        writer.write("Content-Type: text/html\r\n")
        writer.write("Connection: close\r\n\r\n")
        await writer.drain()

        # HTML-Inhalt
        writer.write(response)
        await writer.drain()
        await writer.wait_closed()
    except Exception as e:
        print("Fehler:", e)

async def start_server():
    """Startet den HTTP-Server."""
    server = await asyncio.start_server(serve_client, "0.0.0.0", 80)
    print("Server läuft...")
    async with server:
        await server.serve_forever()

def connect_wifi():
    """Verbindet mit WLAN."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    print("Verbindet mit WLAN...")
    while not wlan.isconnected():
        pass
    print("Verbunden:", wlan.ifconfig())

# Hauptprogramm
connect_wifi()
try:
    asyncio.run(asyncio.gather(update_angles(), start_server()))
except KeyboardInterrupt:
    print("Server gestoppt.")
