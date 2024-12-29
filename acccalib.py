from imu import MPU6050
from machine import Pin, I2C
import time

def calibrate_linear_acceleration(calibration_time=5, axis_label='Z', settling_time=4):
    """
    Calibrate the accelerometer of the MPU6050 by computing the slope (m) and y-intercept (b)
    for linear acceleration calibration.
    
    Parameters:
        calibration_time (int): Time in seconds for each calibration phase.
        axis_label (str): Label of the axis to calibrate ('X', 'Y', or 'Z').
        settling_time (float): Time in seconds to allow the MPU6050 to settle.
    
    Returns:
        tuple: (m, b) - Slope and y-intercept for the calibration.
    """
    # Axis mapping
    axis_map = {'X': 0, 'Y': 1, 'Z': 2}
    if axis_label not in axis_map:
        raise ValueError("Invalid axis label. Choose 'X', 'Y', or 'Z'.")
    axis = axis_map[axis_label]

    # Initialize I2C communication with MPU6050
    i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
    imu = MPU6050(i2c)

    # Prompt user and wait for input before settling
    print(f'\nPrepare the MPU6050 for {axis_label} axis calibration.')
    input('Press Enter when the MPU6050 is in the correct orientation for settling...')
    
    # Allow the MPU6050 to settle
    print(f'Settling MPU for {settling_time} seconds')
    time.sleep(settling_time)
    print('MPU is Done Settling')

    def get_linear_acceleration():
        """
        Get the current linear acceleration readings from the MPU6050.
        
        Returns:
            tuple: (ax, ay, az) - Accelerometer readings on x, y, z axes.
        """
        ax = imu.accel.x
        ay = imu.accel.y
        az = imu.accel.z
        return ax, ay, az

    def collect_data_for_phase(expected_accel, phase_name):
        """
        Collect data for one calibration phase.
        
        Parameters:
            expected_accel (float): Expected acceleration value (e.g., 1, -1, or 0).
            phase_name (str): Name of the calibration phase for printing messages.
        
        Returns:
            tuple: (x_sum, y_sum, x_squared_sum, x_times_y_sum, num_of_points)
        """
        num_of_points = 0
        x_sum = 0
        y_sum = 0
        x_squared_sum = 0
        x_times_y_sum = 0
        
        print(f'\n--- Calibration Phase: {phase_name} ---')
        input('Place the axis in the required position and press Enter when ready...')
        end_loop_time = time.time() + calibration_time
        print(f'Beginning Calibration Phase ({expected_accel}g) for {calibration_time} seconds')
        
        while end_loop_time > time.time():
            num_of_points += 1
            acceleration = get_linear_acceleration()[axis]
            offset = acceleration - expected_accel
            
            x_sum += expected_accel
            y_sum += offset
            x_squared_sum += expected_accel ** 2
            x_times_y_sum += expected_accel * offset
            
            if num_of_points % 100 == 0:
                print(f'Still Calibrating... {num_of_points} points so far')
        
        return x_sum, y_sum, x_squared_sum, x_times_y_sum, num_of_points

    # Collect data for each calibration phase
    x_sum1, y_sum1, x_squared_sum1, x_times_y_sum1, num_of_points1 = collect_data_for_phase(1, f'{axis_label} Upwards')
    x_sum2, y_sum2, x_squared_sum2, x_times_y_sum2, num_of_points2 = collect_data_for_phase(-1, f'{axis_label} Downwards')
    x_sum3, y_sum3, x_squared_sum3, x_times_y_sum3, num_of_points3 = collect_data_for_phase(0, f'{axis_label} Perpendicular')

    # Aggregate data
    total_num_of_points = num_of_points1 + num_of_points2 + num_of_points3
    total_x_sum = x_sum1 + x_sum2 + x_sum3
    total_y_sum = y_sum1 + y_sum2 + y_sum3
    total_x_squared_sum = x_squared_sum1 + x_squared_sum2 + x_squared_sum3
    total_x_times_y_sum = x_times_y_sum1 + x_times_y_sum2 + x_times_y_sum3
    
    # Calculate slope (m) and y-intercept (b)
    m = (total_num_of_points * total_x_times_y_sum - total_x_sum * total_y_sum) / \
        (total_num_of_points * total_x_squared_sum - total_x_sum ** 2)
    b = (total_y_sum - m * total_x_sum) / total_num_of_points
    
    return m, b

# Example usage
if __name__ == "__main__":
    calibTime = 10
    setTime = 4
    
    mx, bx = calibrate_linear_acceleration(calibration_time=calibTime, axis_label='X', settling_time=setTime)
    print()
    print("X Done")
    my, by = calibrate_linear_acceleration(calibration_time=calibTime, axis_label='Y', settling_time=setTime)
    print()
    print("Y Done")
    mz, bz = calibrate_linear_acceleration(calibration_time=calibTime, axis_label='Z', settling_time=setTime)
    print()
    print("Z Done")
    
    
    print()
    print(f'Calibration results X: Slope (m) = {mx:.4f}, Y-Intercept (b) = {bx:.4f}')
    
    print()
    print(f'Calibration results Y: Slope (m) = {my:.4f}, Y-Intercept (b) = {by:.4f}')

    print()
    print(f'Calibration results Z: Slope (m) = {mz:.4f}, Y-Intercept (b) = {bz:.4f}')
