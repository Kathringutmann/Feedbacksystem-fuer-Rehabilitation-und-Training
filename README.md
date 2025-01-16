## Feedbacksystem-fuer-Rehabilitation-und-Training

# verwendete .py:
Ja, mit den vier Python-Dateien (**`imu.py`**, **`kalibrierungs.py`**, **`html.py`** und **`winkelmessungs.py`**) sollte der Code vollständig funktionieren, vorausgesetzt, die Dateien sind korrekt implementiert und erfüllen die jeweiligen Aufgaben. Hier ist eine Erklärung, welche Aufgabe jede Datei hat:

---

### **1. `imu.py`**: 
#### **Aufgabe: Sensor-Interface**
- Diese Datei definiert die **`MPU6050`-Klasse**, die als Schnittstelle zum MPU6050-Sensor dient.
- Sie erlaubt die Initialisierung des Sensors sowie das Auslesen der Beschleunigungs- und Gyroskopdaten.
- Hauptfunktionen:
  - **`init_sensor()`**: Weckt den Sensor aus dem Schlafmodus auf.
  - **`read_accel()`**: Liest die Beschleunigungsdaten (x, y, z) aus.
  - **`read_gyro()`**: Liest die Gyroskopdaten (x, y, z) aus.
  - **`who_am_i()`**: Prüft, ob der Sensor korrekt verbunden ist.

#### **Rolle im Gesamtsystem**:
- Diese Datei abstrahiert die Sensorhardware, sodass andere Teile des Codes die Sensordaten einfach nutzen können.

---

### **2. `kalibrierungs.py`**:
#### **Aufgabe: Sensor-Kalibrierung**
- Diese Datei ist dafür verantwortlich, die Sensoren zu kalibrieren und die Kalibrierungsdaten in einer JSON-Datei zu speichern.
- Hauptbestandteile:
  - **Kalibrierungsprozess**: 
    - Liest die aktuellen Beschleunigungswerte.
    - Berechnet die Offsets für x-, y- und z-Achse (um den Nullpunkt der Sensoren zu justieren).
  - **`save_calibration(data)`**: Speichert die Kalibrierungsdaten in der Datei `calibration.json`.

#### **Rolle im Gesamtsystem**:
- Diese Datei wird verwendet, um die Sensoren einmalig zu kalibrieren, bevor sie für Winkelmessungen verwendet werden.
- Sie stellt sicher, dass die Messdaten der Sensoren genau sind, indem sie systematische Fehler (wie Versatz) korrigiert.

---

### **3. `html.py`**:
#### **Aufgabe: Generierung von HTML**
- Diese Datei enthält die Funktion(en), die das HTML-Dokument für den Webserver generieren.
- Hauptbestandteil:
  - **`generate_html(knee_angle)`**:
    - Nimmt den berechneten Winkel des Kniegelenks als Eingabe.
    - Erstellt eine HTML-Seite, die diesen Winkel anzeigt.
    - Kann zusätzliche Informationen oder Visualisierungen enthalten.

#### **Rolle im Gesamtsystem**:
- Diese Datei wird verwendet, um die Daten aus dem System (insbesondere den gemessenen Winkel) in einer für den Benutzer verständlichen Form darzustellen.
- Sie wird vom Webserver genutzt, um die Webseite dynamisch zu erstellen.

---

### **4. `winkelmessungs.py`**:
#### **Aufgabe: Winkelberechnung und Webserver**
- Diese Datei ist der zentrale Steuerungscode und übernimmt mehrere Aufgaben:
  - **Initialisierung**:
    - Lädt die Kalibrierungsdaten aus der Datei `calibration.json`.
    - Initialisiert die Sensoren mit den Kalibrierungswerten.
  - **Winkelberechnung**:
    - Nutzt die Beschleunigungsdaten beider Sensoren, um den Winkel zwischen den beiden Sensoren (Oberschenkel und Unterschenkel) zu berechnen.
  - **Webserver**:
    - Startet einen einfachen Webserver, der den berechneten Winkel in einer HTML-Seite anzeigt (mit Hilfe von `html.py`).

#### **Rolle im Gesamtsystem**:
- Diese Datei verbindet alle Komponenten:
  - Die Sensor-Daten werden mit **`imu.py`** ausgelesen.
  - Die Kalibrierungsdaten werden mit **`kalibrierungs.py`** genutzt.
  - Die HTML-Seite wird mit **`html.py`** erstellt.
- Sie führt den Hauptprozess aus: Winkelmessung und Anzeige über einen Webserver.

---

### **Zusammenarbeit der Dateien**
1. **`imu.py`**: Bietet die grundlegenden Funktionen für das Lesen von Sensordaten.
2. **`kalibrierungs.py`**: Sorgt dafür, dass die Sensordaten korrekt kalibriert sind.
3. **`html.py`**: Erstellt die HTML-Seite, die die berechneten Daten anzeigt.
4. **`winkelmessungs.py`**: Führt die Winkelmessung aus, steuert den Prozess und verbindet die Daten mit der HTML-Darstellung über den Webserver.

---

### **Ablauf im Gesamtsystem**
1. Die Sensoren werden mit **`imu.py`** angesprochen.
2. Mit **`kalibrierungs.py`** werden die Sensoren kalibriert und die Kalibrierungsdaten gespeichert.
3. Die Winkelberechnung erfolgt in **`winkelmessungs.py`**, indem die Sensordaten (aus `imu.py`) genutzt werden.
4. Die Ergebnisse (Winkelmessung) werden mit **`html.py`** in einer HTML-Seite aufbereitet.
5. Der Benutzer kann die HTML-Seite über den Webserver aufrufen, der in **`winkelmessungs.py`** läuft.

---

### **Zusammenfassung der Aufgaben:**
- **`imu.py`**: Hardware-Schnittstelle für Sensoren.
- **`kalibrierungs.py`**: Sensor-Kalibrierung und Datenkorrektur.
- **`html.py`**: Darstellung der Messergebnisse in HTML.
- **`winkelmessungs.py`**: Hauptprogramm, das alles zusammenführt, den Winkel berechnet und die Ergebnisse über den Webserver bereitstellt.
  
  
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
