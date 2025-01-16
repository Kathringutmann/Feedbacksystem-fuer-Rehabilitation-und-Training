from machine import I2C  # Importiere das 'I2C'-Modul von der 'machine' Bibliothek, um mit dem I2C-Bus zu kommunizieren
import ustruct  # Importiere das 'ustruct'-Modul, um Byte-Daten in Python-Datenstrukturen (wie Integer) umzuwandeln

class MPU6050:
    """
    Diese Klasse stellt eine Schnittstelle zum MPU6050-Beschleunigungssensor und Gyroskop dar.
    Sie ermöglicht das Initialisieren des Sensors und das Auslesen von Beschleunigungs- und Gyroskopdaten.
    """
    
    def __init__(self, i2c, address=0x68):
        """
        Konstruktor für die MPU6050-Klasse.
        
        :param i2c: Das I2C-Objekt, das für die Kommunikation mit dem Sensor verwendet wird
        :param address: Die I2C-Adresse des Sensors (Standard: 0x68)
        """
        self.i2c = i2c  # Speichere das I2C-Objekt
        self.address = address  # Speichere die I2C-Adresse des Sensors
        self.init_sensor()  # Initialisiere den Sensor

    def init_sensor(self):
        """
        Initialisiert den MPU6050-Sensor.
        Setzt den Sensor in den aktiven Modus (der Standardmodus nach dem Start ist im Sleep-Modus).
        """
        # Schreibt in das Register PWR_MGMT_1 (Adresse 0x6B) des Sensors, um den Sleep-Modus zu deaktivieren (Setze den Wert auf 0)
        self.i2c.writeto_mem(self.address, 0x6B, b'\x00')  # PWR_MGMT_1 = 0 (Wake up)

    def read_accel(self):
        """
        Liest die Beschleunigungsdaten vom Sensor.
        
        :returns: Die Beschleunigungswerte für die x-, y- und z-Achse als Ganzzahlen
        """
        # Lese 6 Bytes von den Beschleunigungsdaten (Adresse 0x3B)
        accel_data = self.i2c.readfrom_mem(self.address, 0x3B, 6)
        
        # Entpacke die 6 Byte-Daten in 3 Ganzzahlen für die x-, y- und z-Achse
        x, y, z = ustruct.unpack('>hhh', accel_data)
        
        # Gebe die Beschleunigungswerte als Tuple zurück
        return x, y, z

    def read_gyro(self):
        """
        Liest die Gyroskopdaten vom Sensor.
        
        :returns: Die Gyroskopwerte für die x-, y- und z-Achse als Ganzzahlen
        """
        # Lese 6 Bytes von den Gyroskopdaten (Adresse 0x43)
        gyro_data = self.i2c.readfrom_mem(self.address, 0x43, 6)
        
        # Entpacke die 6 Byte-Daten in 3 Ganzzahlen für die x-, y- und z-Achse
        x, y, z = ustruct.unpack('>hhh', gyro_data)
        
        # Gebe die Gyroskopwerte als Tuple zurück
        return x, y, z

    def who_am_i(self):
        """
        Lese die WHO_AM_I-Adresse des Sensors, um zu überprüfen, ob es sich um einen MPU6050 handelt.
        
        :returns: Die Antwort des Sensors, die entweder 0x68 oder 0x69 sein sollte (entsprechend der I2C-Adresse)
        """
        # Lese den Wert des WHO_AM_I-Registers (Adresse 0x75)
        return self.i2c.readfrom_mem(self.address, 0x75, 1)[0]
