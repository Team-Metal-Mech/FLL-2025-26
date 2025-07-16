from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import StopWatch

left_motor = Motor(Port.E)
right_motor = Motor(Port.F)
hub = PrimeHub
driveBase = DriveBase
stopWatch = StopWatch

def gyro_straight(speed, duration):
  driveBase(left_motor, right_motor, )
  hub.imu.reset_heading()
  stopWatch.reset()
  start_time = stopWatch.time()

  while stopWatch.time() - start_time < duration:
    yaw_angle = hub.imu.heading()
    if yaw_angle > 180:
      out_angle = yaw_angle - 360
    else:
      out_angle = -yaw_angle

    correction = 3 * out_angle

    driveBase.drive(speed, correction)
  
  driveBase.stop()
