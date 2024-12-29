import machine
import ujson
from imu import MPU6050

CALIBRATION_FILE = "calibration.json"

i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21))

# Initialisiere Sensoren mit unterschiedlichen Adressen
sensor1 = MPU6050(i2c, address=0x68)  # Sensor 1
sensor2 = MPU6050(i2c, address=0x69)  # Sensor 2

def calibrate_sensor(sensor, sensor_name):
    print(f"Kalibriere {sensor_name}...")
    accel_data = sensor.read_accel()

    calibration_data = {
        "x_offset": -accel_data[0],
        "y_offset": -accel_data[1],
        "z_offset": 1 - accel_data[2]  # Z-Achse sollte 1g entsprechen
    }

    print(f"{sensor_name} Kalibrierdaten: {calibration_data}")
    return calibration_data

def save_calibration(data):
    with open(CALIBRATION_FILE, "w") as file:
        ujson.dump(data, file)
    print("Kalibrierungsdaten gespeichert.")

def calibrate():
    sensor1_calibration = calibrate_sensor(sensor1, "Sensor 1 (Oberschenkel)")
    sensor2_calibration = calibrate_sensor(sensor2, "Sensor 2 (Unterschenkel)")

    calibration = {
        "sensor_1": sensor1_calibration,
        "sensor_2": sensor2_calibration
    }
    save_calibration(calibration)

calibrate()
