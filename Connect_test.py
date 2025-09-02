from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.tools import wait

hub = PrimeHub()

# 모터 A에 연결
motor = Motor(Port.E)

# 모터를 3초 동안 앞으로 돌림
motor.run(500)
wait(3000)
motor.stop()