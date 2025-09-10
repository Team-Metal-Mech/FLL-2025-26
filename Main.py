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
ST:750
F:50
L:65
F:7
L:17
R:23
B:7
F:7
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
F:20
RA:-100
PR:100
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

  def execute(self, text):
    commands = text.split("\n")
    for command in commands:
      command = command.strip()
      if not command:
        continue
      name, value = command.split(":", 1)
      value = float(value.strip())

      if name == 'SS':  # 직진 속도(mm/s)
        self.driveBase.settings(straight_speed=int(value))

      elif name == 'ST':  # 회전 속도(deg/s)
        self.driveBase.settings(turn_rate=int(value))
        self.turn_speed = int(value)

      elif name == 'SA':  # 악셀러레이션 전진 후진
        self.driveBase.settings(straight_acceleration=int(value))

      elif name == 'TA':  # 악셀러레이션 포인트 턴
        self.driveBase.settings(turn_acceleration=int(value))

      elif name == 'AS':  # 어테치먼트 스피드
        self.arm_speed = int(value)

      elif name == 'F': # 앞으로
        self.driveBase.straight(int(value * 10))

      elif name == 'B': # 뒤로
        self.driveBase.straight(int(-value * 10))

      elif name == 'L': # 왼쪽 턴
        self.driveBase.turn(-value)

      elif name == 'R': # 오른쪽 턴
        self.driveBase.turn(value)

      elif name == 'PR':  # 피봇턴 오른쪽
        self.right.run_angle(self.turn_speed, value)

      elif name == 'PL':  # 피봇턴 왼쪽
        self.left.run_angle(self.turn_speed, value)

      elif name == 'LA':  # 왼쪽 모터
        self.at_left_motor.run_angle(self.arm_speed, value)
      
      elif name == 'RA':  # 오른쪽 모터
        self.at_right_motor.run_angle(self.arm_speed, value)

      elif name == 'W': # wait
        wait(int(value * 1000))


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