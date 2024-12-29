from imu import MPU6050
from machine import I2C, Pin
import time
from math import atan2, sqrt, tan, radians
import math

# Initialize I2C communication with MPU6050 on I2C bus 1, using pins 15 (SCL) and 14 (SDA)
i2c = I2C(0, scl=Pin(15), sda=Pin(14), freq=400000)
imu = MPU6050(i2c)

# Calibration values for the accelerometer, von dem Accellib Code bekommen
ax_mValue, ax_bValue = 0.0021, 0.0032  # Calibration results for X-axis
ay_mValue, ay_bValue = 0.0029, 0.0118  # Calibration results for Y-axis
az_mValue, az_bValue = 0.0109, 0.0116  # Calibration results for Z-axis

# Complementary filter parameters         --- Hier gewichtung Festlegen
alpha = 0.88  # Adjust alpha for balance between gyro and accel (0.98 for gyro dominance)
dt = 0.001  # Time step in seconds (adjust as per your loop timing)

##################################################### IMU DATA START ###############################################################################

# Correction functions for accelerometer values
def getAX():
    return imu.accel.x - (ax_mValue * imu.accel.x + ax_bValue)

def getAY():
    return imu.accel.y - (ay_mValue * imu.accel.y + ay_bValue)

def getAZ():
    return imu.accel.z - (az_mValue * imu.accel.z + az_bValue)

def get_gyro():
    return imu.gyro.x, imu.gyro.y, imu.gyro.z

def gyro_calibration(calibration_time=3):
    print('--' * 25)
    print('Beginning Gyro Calibration - Do not move the MPU6050')

    offsets = [0, 0, 0]
    num_of_points = 0
    end_loop_time = time.time() + calibration_time

    # Initialize percentage tracker
    last_percentage = 0

    while end_loop_time > time.time():
        num_of_points += 1
        (gx, gy, gz) = get_gyro()
        offsets[0] += gx
        offsets[1] += gy
        offsets[2] += gz

        if num_of_points % 100 == 0:
            print(f'Still Calibrating Gyro... {num_of_points} points so far')

    print(f'Calibration for Gyro is Complete! {num_of_points} points total')
    offsets = [i / num_of_points for i in offsets]  # Get mean offsets
    time.sleep(0.1)
    
    return offsets

# Initial angle values
angle_x = 0
angle_y = 0

# Perform gyroscope calibration on startup   --- Ich meine man kann das auch weglassen, aber wenn du den Gyro Drift ausgeichen musst Nutze es ---
gyro_offsets = gyro_calibration(calibration_time=3)  # Calibrate for 3 seconds with a 1-second settling time
offset_gx, offset_gy, offset_gz = gyro_offsets


while True:                #--- Main Loop
    ax = getAX()
    ay = getAY()
    az = getAZ()

    # Calculate angles from accelerometer (pitch and roll)
    pitch_accel = math.atan2(ay, az) * (180 / math.pi)  # Pitch
    roll_accel = math.atan2(-ax, math.sqrt(ay ** 2 + az ** 2)) * (180 / math.pi)  # Roll

    # Read gyroscope data and apply calibration offsets
    gyro_x, gyro_y, gyro_z = get_gyro()
    gyro_x -= offset_gx
    gyro_y -= offset_gy

    # Integrate gyroscope data -> Angle = previous angle + gyro rate * time
    angle_x += gyro_x * dt
    angle_y += gyro_y * dt

    # Complementary filter to combine accelerometer and gyroscope data
    angle_x = alpha * angle_x + (1 - alpha) * pitch_accel  # Angle X is used for pitch --
    angle_y = alpha * angle_y + (1 - alpha) * roll_accel   # Angle Y is used for roll  --

    print(f"Pitch: {angle_x:>5}  |  Roll: {angle_y:>5}", end='\r')
