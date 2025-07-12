from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Stop
from pybricks.tools import wait

#setting the movement motor
motor_a = Motor(Port.A)

Motor.angle(100, 360, Stop.HOLD)

wait(100)
