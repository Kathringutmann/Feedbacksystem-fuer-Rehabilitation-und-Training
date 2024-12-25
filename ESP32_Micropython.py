import time
from machine import Pin, I2C

# I2C-Bus einrichten
i2c = I2C(scl=Pin(22), sda=Pin(21))

# MPU-9250 Adresse und Register-Definitionen
MPU9250_ADDR = 0x68
MPU9250_PWR_MGMT_1 = 0x6B
MPU9250_ACCEL_XOUT_H = 0x3B

# MPU9250 initialisieren
i2c.writeto_mem(MPU9250_ADDR, MPU9250_PWR_MGMT_1, bytes([0]))

def read_accel():
    # Lese Beschleunigungsdaten
    data = i2c.readfrom_mem(MPU9250_ADDR, MPU9250_ACCEL_XOUT_H, 6)
    accel_x = (data[0] << 8) | data[1]
    accel_y = (data[2] << 8) | data[3]
    accel_z = (data[4] << 8) | data[5]
    return accel_x, accel_y, accel_z

# Hauptschleife
while True:
    accel_x, accel_y, accel_z = read_accel()
    print("Beschleunigung X: ", accel_x)
    print("Beschleunigung Y: ", accel_y)
    print("Beschleunigung Z: ", accel_z)
    
    time.sleep(1)
    
    
    
    
import math

def calculate_angle(accel_x, accel_y, accel_z):
    angle = math.degrees(math.atan2(accel_y, accel_z))
    return angle

# Hauptschleife
while True:
    accel_x, accel_y, accel_z = read_accel()
    angle = calculate_angle(accel_x, accel_y, accel_z)
    print("Neigungswinkel: ", angle)
    time.sleep(1)
