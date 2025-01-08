## Feedbacksystem-fuer-Rehabilitation-und-Training

# nicht benutzte Libs oder .py :
- ESP32_Micropython.py
- W-Lan_connection_ESP32.py
- acccalib.py
- barebone.py
  
 # Wechsel ziwschen Branches:
 - Auflisten aller Branches: git branch -a
 - Wechsel zu Branch: git checkout -b "Webserver-(einfache-Lösung)" origin/"Webserver-(einfache-Lösung)"
 -  Wechsel zu Main: git checkout main
  
# 1. Code für den ESP32 Kalibrierung (MicroPython: Kalibrierung_Knie.py)
Über drei Achsen Beschläunigung wird jeweils pro Sensor ein Vektor erstellt und deren Abhängigkeit zwischen der beiden, also den Winkel den die beiden zueinander haben 0° gesetzt.

# 2. Code für den ESP32 Winkelmessung (MicroPython: Winkelmessung_MPU6050.py)
Nutzt calibration.json für Messung der Winkel zwischen zwei Vektoren ausgehend von dem gespeicherten 0° Winkel. 

# 3. Code für den ESP32 IMU-Lib (MicroPython: imu.py)
angepasste Lib für die Sensoren (Quelle: Github)

# 4. Code für die Streamlit-App (Python: Trainer_App.py)
Der Streamlit-Code empfängt die Sensordaten über WLAN und zeigt sie in einer Benutzeroberfläche an.
Dropdownmenü für mögliche weitere Gelenke...

# mathematische Erklärung der Winkelmessung (Code: #2)
Der Code berechnet den **Winkel zwischen den beiden MPU6050-Sensoren**, indem er ihre Beschleunigungsdaten nutzt. Hier ist die genaue Funktionsweise Schritt für Schritt erklärt:

---

### **1. Kalibrierung**
- Der Code lädt zuvor gespeicherte **Kalibrierungsdaten** aus einer Datei `calibration.json`. Diese Daten enthalten die Offsets für jeden Sensor, die während einer Kalibrierungsphase ermittelt wurden.
- Die Funktion `apply_calibration` setzt diese Offsets, um systematische Fehler (z. B. falsche Nullpunkte) der Sensoren zu korrigieren.

---

### **2. Winkelberechnung**

#### **a) Beschleunigungsdaten**
- Die Methode `sensor.read_accel()` liefert die Beschleunigungsdaten der Achsen \( X, Y, Z \) für jeden Sensor.
  - \( \text{acc1} \): Daten von Sensor 1.
  - \( \text{acc2} \): Daten von Sensor 2.

#### **b) Normierung**
- Die Vektoren der Beschleunigungsdaten werden **normiert**. Normierung bedeutet, dass der Vektor auf eine Länge von 1 skaliert wird:
  \[
  \text{normierter Vektor} = \left[\frac{x}{|\vec{v}|}, \frac{y}{|\vec{v}|}, \frac{z}{|\vec{v}|}\right]
  \]
  Hierbei ist \( |\vec{v}| \) die Länge (Magnitude) des Vektors:
  \[
  |\vec{v}| = \sqrt{x^2 + y^2 + z^2}
  \]

#### **c) Skalarprodukt**
- Das **Skalarprodukt** zweier Vektoren \( \vec{v_1} \) und \( \vec{v_2} \) wird berechnet:
  \[
  \vec{v_1} \cdot \vec{v_2} = v_{1x} \cdot v_{2x} + v_{1y} \cdot v_{2y} + v_{1z} \cdot v_{2z}
  \]
- Das Skalarprodukt misst, wie „ähnlich“ oder „parallel“ die beiden Vektoren sind. Es liefert einen Wert zwischen \(-1\) (entgegengesetzt) und \(+1\) (parallel).

#### **d) Winkelberechnung**
- Der Winkel \( \theta \) zwischen den beiden Vektoren wird aus dem Skalarprodukt bestimmt:
  \[
  \cos(\theta) = \frac{\vec{v_1} \cdot \vec{v_2}}{|\vec{v_1}| \cdot |\vec{v_2}|}
  \]
  Da die Vektoren bereits normiert sind (\( |\vec{v_1}| = |\vec{v_2}| = 1 \)), vereinfacht sich die Formel zu:
  \[
  \cos(\theta) = \vec{v_1} \cdot \vec{v_2}
  \]
- Der Winkel wird mit dem Arkuskosinus (\( \arccos \)) berechnet:
  \[
  \theta = \arccos(\cos(\theta))
  \]
- Um den Winkel in Grad umzurechnen:
  \[
  \text{Winkel (in Grad)} = \text{degrees}(\theta)
  \]

#### **e) Einschränkung numerischer Ungenauigkeiten**
- Aufgrund von Rundungsfehlern kann das Skalarprodukt Werte minimal außerhalb des Bereichs \([-1, 1]\) annehmen, was zu einem Fehler bei der Berechnung von \( \arccos \) führen würde. Deshalb wird der Wert begrenzt:
  \[
  \cos(\theta) = \text{max}(\text{min}(\vec{v_1} \cdot \vec{v_2}, 1.0), -1.0)
  \]

---

### **3. Hauptschleife**
- Der Winkel zwischen den beiden Sensoren wird fortlaufend berechnet und ausgegeben.
- Die Messungen erfolgen in einem Intervall von 500 ms.

---

### **Zusammengefasst**
Der Winkel wird folgendermaßen bestimmt:
1. Die Beschleunigungsvektoren der beiden Sensoren werden abgerufen.
2. Diese Vektoren werden normiert.
3. Das Skalarprodukt der normierten Vektoren wird berechnet.
4. Der Winkel zwischen den Vektoren wird über den Arkuskosinus berechnet.
5. Das Ergebnis wird in Grad ausgegeben.

Dieser Ansatz ermöglicht die **Messung relativer Winkel** zwischen zwei Körperteilen (z. B. Oberschenkel und Unterschenkel). Der Code ist präzise für statische oder langsam bewegte Systeme. Für schnelle Bewegungen könnte die Nutzung der Gyroskopdaten (in Kombination mit einem Filter) hinzugefügt werden.


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
