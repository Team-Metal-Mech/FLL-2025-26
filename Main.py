from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Button
from pybricks.robotics import DriveBase
from pybricks.tools import wait


WHEEL_DIAMETER_MM = 62.4
AXLE_TRACK_MM = 140

# 기본 속도/가속도 값(직접 단위 사용)
DEFAULT_STRAIGHT_SPEED = 150   # mm/s
DEFAULT_STRAIGHT_ACCEL = 300   # mm/s^2
DEFAULT_TURN_RATE = 180        # deg/s
DEFAULT_TURN_ACCEL = 180       # deg/s^2

movement1 = """
SS:700
SA:1000
ST:750
TA:900
AS:700
RA:-29
F:64
L:125
TA:500
R:26
B:9
F:9
AS:400
RA:-28
R:100
AS:600
RA:28
F:15
L:60
B:8
R:3
F:9
RA:-28
L:3
F:6
"""
movement2 = """
SS:150
ST:180
F:25
R:90
F:25
R:90
F:25
R:90
F:25
"""
movement3 = """
SS:700
ST:700
SA:2000
AS:700
F:10000
"""

class MetalMechRobot:
  def __init__(self):
    self.hub = PrimeHub()
    self.left = Motor(Port.E, Direction.COUNTERCLOCKWISE)
    self.right = Motor(Port.F)
    self.driveBase = DriveBase(self.left, self.right, WHEEL_DIAMETER_MM, AXLE_TRACK_MM)
    self.at_left_motor = Motor(Port.C)
    self.at_right_motor = Motor(Port.D)
    self.turn_speed = 200
    # 기본 설정 적용
    self.driveBase.settings(straight_speed=DEFAULT_STRAIGHT_SPEED,
                     straight_acceleration=DEFAULT_STRAIGHT_ACCEL,
                     turn_rate=DEFAULT_TURN_RATE,
                     turn_acceleration=DEFAULT_TURN_ACCEL)

    self.driveBase.use_gyro(True)

  def set_straight_speed(self, value):
    self.driveBase.settings(straight_speed=int(value))

  def turn_speed(self, value):
    self.driveBase.settings(turn_rate=int(value))
    self.turn_speed = int(value)
  
  def straight_acceleration_speed(self, value):
    self.driveBase.settings(straight_acceleration=int(value))
  
  def turn_acceleration_speed(self, value):
    self.driveBase.settings(turn_acceleration=int(value))

  def arm_speed(self, value):
    self.arm_speed = int(value)

  def forward(self, value):
    self.driveBase.straight(int(value * 10))

  def backward(self, value):
    self.driveBase.straight(int(-value * 10))

  def left_turn(self, value):
    self.driveBase.turn(-value)

  def right_turn(self, value):
    self.driveBase.turn(value)

  def point_right(self, value):
    self.right.run_angle(self.turn_speed, value)

  def point_left(self, value):
    self.left.run_angle(self.turn_speed, value)

  def left_arm_turn(self, value):
    self.at_left_motor.run_angle(self.arm_speed, value)

  def right_arm_turn(self, value):
    self.at_right_motor.run_angle(self.arm_speed, value)

  def wait(self, value):
    wait(int(value * 1000))


  def execute(self, text):
    commands = text.split("\n")
    for command in commands:
      command = command.strip()
      if not command:
        continue
      name, value = command.split(":", 1)
      value = float(value.strip())

      if name == 'SS':  self.set_straight_speed(value)

      elif name == 'ST':  self.turn_speed(value)
        
      elif name == 'SA':  self.straight_acceleration_speed(value)

      elif name == 'TA':  self.turn_acceleration_speed(value)

      elif name == 'AS':  self.arm_speed(value)

      elif name == 'F': self.forward(value)

      elif name == 'B': self.backward(value)

      elif name == 'L': self.left_turn(value)

      elif name == 'R': self.right_turn(value)

      elif name == 'PR':  self.point_right(value) 

      elif name == 'PL':  self.point_left(value)

      elif name == 'LA':  self.Left_arm_turn(value)
      
      elif name == 'RA':  self.right_arm_turn(value)

      elif name == 'W': self.wait(value)

def wait_for_button_release(hub):
  while True:
    pressed = hub.buttons.pressed()
    if len(pressed) == 0:
      break
    wait(300)

robot = MetalMechRobot()
hub = robot.hub

# 선택 번호: 0은 종료, 1..MAX_SEL은 프로그램 번호
MAX_SEL = 3
selected = 1

while True:
  hub.display.number(selected)

  while True:
    p = hub.buttons.pressed()
    if (Button.LEFT in p) and (Button.RIGHT in p):
      wait_for_button_release(hub)
      break
    if Button.LEFT in p:
      selected = selected - 1
      if selected < 0:
        selected = MAX_SEL
      hub.display.number(selected)
      wait_for_button_release(hub)
    elif Button.RIGHT in p:
      selected = selected + 1
      if selected > MAX_SEL:
        selected = 0
      hub.display.number(selected)
      wait_for_button_release(hub)

    wait(50)

  # CENTER 처리
  if selected == 0:
    break
  else:
    # 선택된 프로그램 실행 후 다시 선택화면으로
    if selected == 1:
      robot.execute(movement1)
    elif selected == 2:
      robot.execute(movement2)
    elif selected == 3:
      robot.execute(movement3)
    wait(300)