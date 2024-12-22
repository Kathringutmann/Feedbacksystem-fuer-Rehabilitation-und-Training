## Feedbacksystem-fuer-Rehabilitation-und-Training


# 1. Code für den ESP32 (MicroPython)
Dieser Code übernimmt das Abrufen der IMU-Daten (z. B. BNO055), die WLAN-Verbindung und das Senden der Daten an die Streamlit-App.
Erklärung:

Der Code stellt eine WLAN-Verbindung her und startet einen Server auf dem ESP32, der auf Anfragen wartet.
Sobald ein Client (die Streamlit-App) verbunden ist, sendet der ESP32 die Euler-Winkel (Roll, Pitch, Yaw) des IMUs.
Du kannst die Pin-Nummern und WLAN-Daten entsprechend deinem Setup anpassen.

# 2. Code für die Streamlit-App
Der Streamlit-Code empfängt die Sensordaten über WLAN und zeigt sie in einer Benutzeroberfläche an

Erklärung:
Die App verbindet sich über WLAN mit dem ESP32 und empfängt kontinuierlich die Daten.
Die Euler-Winkel (Roll, Pitch, Yaw) werden in Echtzeit angezeigt und aktualisiert.
Stelle sicher, dass du die IP-Adresse des ESP32 korrekt in der connect_to_esp32()-Funktion einträgst.


# 3.Wi-Fi Kommunikation (Direkte Verbindung)
Wenn du Wi-Fi bevorzugst und dein IMU über eine eigene Wi-Fi-Konnektivität oder einen eingebauten Mikrocontroller wie den ESP8266 oder ESP32 verfügt, könnte die Kommunikation direkt über Wi-Fi erfolgen. In diesem Fall wäre der ESP32 sowohl der Wi-Fi-Client als auch der Server, der Daten vom IMU empfängt.

Vorteile von Wi-Fi:
Größere Reichweite: Wi-Fi bietet eine größere Reichweite (bis zu mehreren hundert Metern in offenen Bereichen) im Vergleich zu BLE.
Höhere Bandbreite: Du kannst größere Datenmengen über Wi-Fi übertragen, was bei komplexeren IMU-Daten von Vorteil sein kann.
Wie man Wi-Fi verwendet:
IMU mit Wi-Fi-Modul: Ein IMU, das mit einem ESP32 oder ESP8266 verbunden ist, kann die Messdaten über Wi-Fi an den ESP32 senden. Der ESP32 empfängt diese Daten und überträgt sie dann an die Streamlit-App oder an ein anderes Gerät.

ESP32 als Wi-Fi-Client und Server: Der ESP32 könnte über UDP oder TCP mit dem IMU über Wi-Fi kommunizieren, und du kannst dieselbe WLAN-Verbindung wie für die Streamlit-App verwenden.
