from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import StopWatch

left_motor = Motor(Port.E)
right_motor = Motor(Port.F)

def gyro_straight(speed, duration):
  DriveBase(left_motor, right_motor, )
  PrimeHub.imu.reset_heading()
  StopWatch.reset()
  start_time = StopWatch.time()

  while StopWatch.time() - start_time < duration:
    error = -PrimeHub.imu.heading()
    correction = 3 * error

    DriveBase.drive(speed, correction)
  
  DriveBase.stop()
