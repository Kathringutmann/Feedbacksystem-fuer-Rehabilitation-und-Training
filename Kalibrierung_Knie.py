import machine  # Importiere das 'machine'-Modul, das Funktionen für die Steuerung der Hardware bereitstellt
import ujson     # Importiere das 'ujson'-Modul für schnelles JSON-Parsen und -Serialisieren
from imu import MPU6050  # Importiere das MPU6050-Modul für die Kommunikation mit den MPU6050-Sensoren

CALIBRATION_FILE = "calibration.json"  # Definiere den Dateinamen für die Speicherung der Kalibrierungsdaten

# Initialisiere den I2C-Bus, wobei Pin 22 als SCL und Pin 21 als SDA verwendet werden
i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21))

# Initialisiere zwei MPU6050-Sensoren mit unterschiedlichen I2C-Adressen
sensor1 = MPU6050(i2c, address=0x68)  # Sensor 1 (oberschenkel)
sensor2 = MPU6050(i2c, address=0x69)  # Sensor 2 (Unterschenkel)

def calibrate_sensor(sensor, sensor_name):
    """
    Kalibriert einen Sensor, indem es die aktuellen Beschleunigungsdaten liest und Offset-Werte berechnet.
    """
    print(f"Kalibriere {sensor_name}...")  # Zeige an, welcher Sensor gerade kalibriert wird
    
    # Lese die aktuellen Beschleunigungsdaten des Sensors
    accel_data = sensor.read_accel()
    
    # Berechne die Kalibrierungsdaten: Offset-Werte für x, y und z
    calibration_data = {
        "x_offset": -accel_data[0],  # Das Negieren des x-Werts als Offset
        "y_offset": -accel_data[1],  # Das Negieren des y-Werts als Offset
        "z_offset": 1 - accel_data[2]  # Der z-Wert sollte 1g entsprechen, also wird 1 minus dem gemessenen Wert als Offset verwendet
    }
    
    print(f"{sensor_name} Kalibrierdaten: {calibration_data}")  # Gib die Kalibrierungsdaten des Sensors aus
    
    # Gib die berechneten Kalibrierungsdaten zurück
    return calibration_data

def save_calibration(data):
    """
    Speichert die Kalibrierungsdaten in einer JSON-Datei.
    """
    with open(CALIBRATION_FILE, "w") as file:
        ujson.dump(data, file)  # Speichere die Kalibrierungsdaten im JSON-Format in der Datei
    print("Kalibrierungsdaten gespeichert.")  # Bestätige, dass die Daten gespeichert wurden

def calibrate():
    """
    Kalibriert beide Sensoren und speichert die Kalibrierungsdaten.
    """
    # Kalibriere Sensor 1 (Oberschenkel) und Sensor 2 (Unterschenkel)
    sensor1_calibration = calibrate_sensor(sensor1, "Sensor 1 (Oberschenkel)")
    sensor2_calibration = calibrate_sensor(sensor2, "Sensor 2 (Unterschenkel)")
    
    # Erstelle ein Dictionary, das die Kalibrierungsdaten für beide Sensoren enthält
    calibration = {
        "sensor_1": sensor1_calibration,
        "sensor_2": sensor2_calibration
    }
    
    # Speichere die Kalibrierungsdaten in einer JSON-Datei
    save_calibration(calibration)

# Starte den Kalibrierungsprozess
calibrate()
