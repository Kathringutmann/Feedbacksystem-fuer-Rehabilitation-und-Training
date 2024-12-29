import machine
import math
import json
from imu import MPU6050

# I2C-Einstellungen
i2c = machine.I2C(1, scl=machine.Pin(22), sda=machine.Pin(21))

# Sensoren initialisieren
sensor_1 = MPU6050(i2c, address=0x68)
sensor_2 = MPU6050(i2c, address=0x69)

# Kalibrierungsdaten laden
with open("calibration.json", "r") as f:
    calibration_data = json.load(f)

sensor_1_offsets = calibration_data["sensor_1"]
sensor_2_offsets = calibration_data["sensor_2"]

# Kalibrierungswerte anwenden
def apply_calibration(sensor, offsets):
    sensor.x_offset = offsets["x_offset"]
    sensor.y_offset = offsets["y_offset"]
    sensor.z_offset = offsets["z_offset"]

apply_calibration(sensor_1, sensor_1_offsets)
apply_calibration(sensor_2, sensor_2_offsets)

# Funktion zur Winkelberechnung
def calculate_angle(sensor_1, sensor_2):
    # Beschleunigungsdaten abrufen
    acc1 = sensor_1.read_accel()
    acc2 = sensor_2.read_accel()

    
    # Normierte Vektoren berechnen
    def normalize(vector):
        magnitude = math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)
        return [v / magnitude for v in vector]
    v1 = normalize([acc1[0], acc1[1], acc1[2]])
    v2 = normalize([acc2[0], acc2[1], acc2[2]])

    
    # Skalarprodukt berechnen
    dot_product = sum(v1[i] * v2[i] for i in range(3))
    
    # Winkel berechnen (im Bogenmaß und dann in Grad umrechnen)
    angle_rad = math.acos(max(min(dot_product, 1.0), -1.0))  # Klammern, um numerische Ungenauigkeiten zu vermeiden
    angle_deg = math.degrees(angle_rad)
    
    return angle_deg

# Hauptschleife
print("Starte Winkelmessung. Bewege das Bein...")
while True:
    try:
        angle = calculate_angle(sensor_1, sensor_2)
        print("Winkel: {:.2f}°".format(angle))
        machine.sleep(500)  # Ausgabe alle 500ms
    except KeyboardInterrupt:
        print("Messung beendet.")
        break
