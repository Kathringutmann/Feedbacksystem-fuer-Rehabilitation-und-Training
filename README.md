## Feedbacksystem-fuer-Rehabilitation-und-Training

# nicht benutzte Libs oder .py :
- ESP32_Micropython.py
- W-Lan_connection_ESP32.py
- acccalib.py
- barebone.py
  
  
# 1. Code für den ESP32 Kalibrierung (MicroPython: Kalibrierung_Knie.py)
Über drei Achsen Beschläunigung wird jeweils pro Sensor ein Vektor erstellt und deren Abhängigkeit zwischen der beiden, also den Winkel den die beiden zueinander haben 0° gesetzt.

# 2. Code für den ESP32 Winkelmessung (MicroPython: Winkelmessung_MPU6050.py)
Nutzt calibration.json für Messung der Winkel zwischen zwei Vektoren ausgehend von dem gespeicherten 0° Winkel. 

# 3. Code für den ESP32 IMU-Lib (MicroPython: imu.py)
angepasste Lib für die Sensoren (Quelle: Github)

# 4. Code für die Streamlit-App (Python: Trainer_App.py)
Der Streamlit-Code empfängt die Sensordaten über WLAN und zeigt sie in einer Benutzeroberfläche an.
Dropdownmenü für mögliche weitere Gelenke...


# Anwendung:
1. Kalibrierung direkt in "Endlage = 0°" des Gelenks für jede Benutzung seperat
2. Ausführung Code zur Winkelmessung
3. Ausgabe auf Webserver oder App...?
   

# To do's
- Webserverhandshake zwischen Streamlit App und Winkelmessung vom ESP32
- Stromversorgung über Laptop?

# mögliche Erweiterungen
- mögliche Halterungen (3D-Druck) zur Erweiterung für mehr Gelenksmessungen
- App Erweiterung der Gelenke
- App Erweiterung für Kommunikation mit Physios,...
   Ziel: nur Sensoren an Gelenken und Anzeige in der App zur Hilfe bei Eigenmobilisation odeer Winkelkontrolle
