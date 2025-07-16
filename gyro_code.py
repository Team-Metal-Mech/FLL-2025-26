# Importing every tools that we need for the program
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import StopWatch

# Putting all the classes to variable
left_motor = Motor(Port.E)
right_motor = Motor(Port.F)
hub = PrimeHub
driveBase = DriveBase
stopWatch = StopWatch

# Function created
def gyro_straight(speed, duration):
  # We still need to measure the robot's dimensions
  driveBase(left_motor, right_motor, )
  # Reset yaw angle
  hub.imu.reset_heading()
  # Reseting the stopwatch
  stopWatch.reset()
  start_time = stopWatch.time()

  # While loop
  while stopWatch.time() - start_time < duration:
    # Variable named yaw_angle equal to current yaw angle
    yaw_angle = hub.imu.heading()
    # line 30 to 33 is the command which sets the out_angle which is error
    if yaw_angle > 180:
      out_angle = yaw_angle - 360
    else:
      out_angle = -yaw_angle

    correction = 3 * out_angle

    # Go straight
    driveBase.drive(speed, correction)

  # Stop the Robot  
  driveBase.stop()
