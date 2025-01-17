## Feedbacksystem-fuer-Rehabilitation-und-Training

# Feedbacksystem für Rehabilitation und Training

Dieses Projekt misst den Kniegelenkswinkel in Echtzeit und stellt die Daten über einen Webserver zur Verfügung. Es wurde für Rehabilitation und Training entwickelt und verwendet ESP32 sowie MPU6050-Sensoren.

## Inhaltsverzeichnis
- [Systemübersicht](#systemübersicht)
- [Hardware](#hardware)
- [Software](#software)
- [Einrichtung](#einrichtung)
- [Verwendung](#verwendung)
- [BOM (Bill of Materials)](#bom-bill-of-materials)
- [Softwarearchitektur](#Softwarearchitektur).
- [mögliche-Erweiterungen](#mögliche-Erweiterungen)

## Systemübersicht

Das System verwendet zwei MPU6050-Sensoren, um den Winkel eines Kniegelenks zu messen. Der ESP32 fungiert als Hauptprozessor, verbindet sich mit dem WLAN und stellt die Messergebnisse über einen Webserver bereit. Der Benutzer kann die aktuellen Daten in einem Browser anzeigen.

## Hardware

### Erforderliche Komponenten
- ESP32 Mikrocontroller
- Zwei MPU6050-Sensoren
- I2C-Kabel
- Stromversorgung (z. B. USB-Kabel)
- Kniegelenk-Halterung

Details zur genauen Stückliste im Abschnitt [BOM](#bom-bill-of-materials).

## Software

Die Firmware basiert auf Micropython und enthält die MPU6050-Bibliothek. Der Code verbindet sich mit einem definierten WLAN-Netzwerk und zeigt den aktuellen Kniegelenkswinkel über eine Webseite an.

### Installation von Micropython
1. Flashen Sie die Micropython-Firmware auf den ESP32:
2. Laden Sie den Code (siehe Repository) auf den ESP32.

### WLAN-Konfiguration
Passen Sie die Variablen `ssid` und `password` im Code an Ihr WLAN an.

## Einrichtung

1. Verbinde MPU6050-Sensoren mit dem ESP32:
- SDA an Pin 21
- SCL an Pin 22
2. Stromversorgung anschließen.
3. Starten des ESP32.

## Verwendung

- Der Webserver läuft unter der IP-Adresse des ESP32 (im Terminal angezeigt).
- Öffnen Sie die Adresse in einem Browser, um den aktuellen Kniegelenkswinkel zu sehen.

## BOM (Bill of Materials)

### Hardware
| **Komponente**       | **Beschreibung**                                                | **Menge** | **Bezugsquelle** (optional) |
|-----------------------|----------------------------------------------------------------|-----------|-----------------------------|
| **ESP32 Mikrocontroller** | Mikrocontroller für die WLAN- und Sensorverarbeitung       | 1         | Uni |
| **MPU6050 IMU**       | Beschleunigungs- und Gyroskopsensor (zwei Stück für die Kniegelenksmessung) | 2         | Freund |
| **I2C-Verbindungskabel** | Verbindungskabel für I2C-Kommunikation zwischen ESP32 und MPU6050 | 4         | Uni         |
| **Stromversorgung**   | USB-Kabel oder Batteriehalterung (abhängig von deinem Setup)  | 1         | Uni         |
| **Kniegelenk-Halterung** | Halterung, um die Sensoren am Knie zu befestigen            | 1         | 3D-Druck           |

### Software
| **Komponente**        | **Beschreibung**                                              | **Version** (falls bekannt) | **Bezugsquelle**            |
|-----------------------|----------------------------------------------------------------|-----------------------------|-----------------------------|
| **Micropython**       | Firmware für den ESP32                                        | Aktuell                     | [Micropython](https://micropython.org/) |
| **MPU6050 Library**   | Python-Bibliothek für die Kommunikation mit dem MPU6050       | -                           | Enthalten in deinem Code   |
| **JSON-Modul**        | Standard-Python-Modul für JSON-Verarbeitung                   | -                           | Standard                    |
| **WLAN-Konfiguration**| SSID und Passwort im Code festgelegt                          | -                           | Benutzerdefiniert           |

---
### **Softwarearchitektur**
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

### **2. `Kalibrierung_Knie.py`**:
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

### **3. `html_template.py`**:
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

### **4. `Winkelmessung-mit_Webserver.py`**:
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
  - Die Kalibrierungsdaten werden mit **`Kalibrierung_Knie.py`** genutzt.
  - Die HTML-Seite wird mit **`html_template.py`** erstellt.
- Sie führt den Hauptprozess aus: Winkelmessung und Anzeige über einen Webserver.

---

### **Zusammenarbeit der Dateien**
1. **`imu.py`**: Bietet die grundlegenden Funktionen für das Lesen von Sensordaten.
2. **`Kalibrierung_Knie.py`**: Sorgt dafür, dass die Sensordaten korrekt kalibriert sind.
3. **`html_template.py`**: Erstellt die HTML-Seite, die die berechneten Daten anzeigt.
4. **`Winkelmessung_mit_Webserver.py`**: Führt die Winkelmessung aus, steuert den Prozess und verbindet die Daten mit der HTML-Darstellung über den Webserver.

---

### **Ablauf im Gesamtsystem**
1. Die Sensoren werden mit **`imu.py`** angesprochen.
2. Mit **`Kalibrierung_Knie.py`** werden die Sensoren kalibriert und die Kalibrierungsdaten gespeichert.
3. Die Winkelberechnung erfolgt in **`Winkelmessung_mit_Webserver.py`**, indem die Sensordaten (aus `imu.py`) genutzt werden.
4. Die Ergebnisse (Winkelmessung) werden mit **`html.py`** in einer HTML-Seite aufbereitet.
5. Der Benutzer kann die HTML-Seite über den Webserver aufrufen, der in **`Winkelmessung_mit_Webserver.py`** läuft.

---

### **Zusammenfassung der Aufgaben:**
- **`imu.py`**: Hardware-Schnittstelle für Sensoren.
- **`Kalibrierung_Knie.py`**: Sensor-Kalibrierung und Datenkorrektur.
- **`html_template.py`**: Darstellung der Messergebnisse in HTML.
- **`Winkelmessung_mit_Webserver.py`**: Hauptprogramm, das alles zusammenführt, den Winkel berechnet und die Ergebnisse über den Webserver bereitstellt.
  
---



# mögliche Erweiterungen
- mögliche Halterungen (3D-Druck) zur Erweiterung für mehr Gelenksmessungen
- Stromversorgung unabhängig von Laptop
- App(Streamlit,... statt Webserver)
- App Erweiterung der Gelenke
- App Erweiterung für Kommunikation mit Physios,...

---
Ziel: nur Sensoren an Gelenken und Anzeige in der App zur Hilfe bei Eigenmobilisation odeer Winkelkontrolle beim eigenständigen Krafttraining
