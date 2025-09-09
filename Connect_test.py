from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Stop
from pybricks.tools import wait
from pybricks.robotics import DriveBase

hub = PrimeHub()
stop = Stop
left_motor = Motor(Port.E, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.F)
drivebase = DriveBase(left_motor, right_motor, 62.4, 140)
drivebase.settings(500)
hub.imu.reset_heading(0)
drivebase.use_gyro(True)

drivebase.straight(100, stop.COAST)
wait(10)

drivebase.turn(-50, stop.COAST)
wait(20)

drivebase.straight(300, stop.COAST)
wait(10)

left_motor.reset_angle(300)

