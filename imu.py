from machine import I2C
import ustruct

class MPU6050:
    def __init__(self, i2c, address=0x68):
        self.i2c = i2c
        self.address = address
        self.init_sensor()

    def init_sensor(self):
        # Setze den Sensor in den aktiven Modus
        self.i2c.writeto_mem(self.address, 0x6B, b'\x00')  # PWR_MGMT_1 = 0 (Wake up)

    def read_accel(self):
        # Lese Beschleunigungsdaten (6 Bytes)
        accel_data = self.i2c.readfrom_mem(self.address, 0x3B, 6)
        x, y, z = ustruct.unpack('>hhh', accel_data)
        return x, y, z

    def read_gyro(self):
        # Lese Gyroskopdaten (6 Bytes)
        gyro_data = self.i2c.readfrom_mem(self.address, 0x43, 6)
        x, y, z = ustruct.unpack('>hhh', gyro_data)
        return x, y, z

    def who_am_i(self):
        # Lese die WHO_AM_I-Adresse (sollte 0x68 oder 0x69 sein)
        return self.i2c.readfrom_mem(self.address, 0x75, 1)[0]
