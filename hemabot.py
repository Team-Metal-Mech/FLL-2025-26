from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase
from pybricks.tools import wait


WHEEL_DIAMETER_MM = 62
AXLE_TRACK_MM = 149

# 기본 속도/가속도 값(직접 단위 사용)
DEFAULT_STRAIGHT_SPEED = 150   # mm/s
DEFAULT_STRAIGHT_ACCEL = 300   # mm/s^2
DEFAULT_TURN_RATE = 180        # deg/s
DEFAULT_TURN_ACCEL = 180       # deg/s^2

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

  def set_straight_speed(self, value):
    self.driveBase.settings(straight_speed=int(value))

  def set_turn_speed(self, value):
    self.driveBase.settings(turn_rate=int(value))
    self.turn_speed = int(value)
  
  def set_straight_acceleration_speed(self, value):
    self.driveBase.settings(straight_acceleration=int(value))
  
  def set_turn_acceleration_speed(self, value):
    self.driveBase.settings(turn_acceleration=int(value))

  def set_arm_speed(self, value):
    self.arm_speed = int(value)

  def do_forward(self, value):
    self.driveBase.straight(int(value * 10))
    wait(50)

  def do_backward(self, value):
    self.driveBase.straight(int(-value * 10))
    wait(50)

  def do_left_turn(self, value):
    self.driveBase.turn(-value)
    wait(50)
  
  def do_right_turn(self, value):
    self.driveBase.turn(value)
    wait(50)
  
  def do_point_right(self, value):
    self.right.run_angle(self.turn_speed, value)
    wait(50)
  
  def do_point_left(self, value):
    self.left.run_angle(self.turn_speed, value)
    wait(50)
  
  def do_left_arm_turn(self, value, nonblock=False):
    # nonblock=True이면 즉시 반환(wait=False)
    self.at_left_motor.run_angle(self.arm_speed, value, wait=(not nonblock))
    if not nonblock:
      wait(50)
  
  def do_right_arm_turn(self, value, nonblock=False):
    # nonblock=True이면 즉시 반환(wait=False)
    self.at_right_motor.run_angle(self.arm_speed, value, wait=(not nonblock))
    if not nonblock:
      wait(50)

  def do_arms_turn(self, left_value, right_value=None):
    # 양팔을 동시에 회전. 한 값만 주면 두 팔에 동일 적용.
    if right_value is None:
      right_value = left_value

    # 더 오래 걸리는 쪽을 wait=True로 두어 두 모터 모두 완료될 때까지 대기
    if abs(left_value) >= abs(right_value):
      # 왼쪽이 더 오래 걸릴 가능성이 큼: 오른쪽 먼저(비대기), 왼쪽 대기
      self.at_right_motor.run_angle(self.arm_speed, right_value, wait=False)
      self.at_left_motor.run_angle(self.arm_speed, left_value, wait=True)
    else:
      # 오른쪽이 더 오래 걸릴 가능성이 큼: 왼쪽 먼저(비대기), 오른쪽 대기
      self.at_left_motor.run_angle(self.arm_speed, left_value, wait=False)
      self.at_right_motor.run_angle(self.arm_speed, right_value, wait=True)
    wait(50)

  def execute(self, text):
    self.driveBase.use_gyro(True)
    commands = text.split("#")
    for command in commands:
      command = command.strip()
      if not command:
        continue
      parts = [p.strip() for p in command.split(":")]
      if len(parts) == 0:
        continue
      name = parts[0]
      args = parts[1:]

      if name == 'SS' and len(args) >= 1:
        self.set_straight_speed(float(args[0]))

      elif name == 'ST' and len(args) >= 1:
        self.set_turn_speed(float(args[0]))
        
      elif name == 'SA' and len(args) >= 1:
        self.set_straight_acceleration_speed(float(args[0]))

      elif name == 'TA' and len(args) >= 1:
        self.set_turn_acceleration_speed(float(args[0]))

      elif name == 'AS' and len(args) >= 1:
        self.set_arm_speed(float(args[0]))

      elif name == 'F' and len(args) >= 1:
        self.do_forward(float(args[0]))

      elif name == 'B' and len(args) >= 1:
        self.do_backward(float(args[0]))

      elif name == 'L' and len(args) >= 1:
        self.do_left_turn(float(args[0]))

      elif name == 'R' and len(args) >= 1:
        self.do_right_turn(float(args[0]))

      elif name == 'PR' and len(args) >= 1:
        self.do_point_right(float(args[0])) 

      elif name == 'PL' and len(args) >= 1:
        self.do_point_left(float(args[0]))

      elif name == 'LA' and len(args) >= 1:
        angle = float(args[0])
        nonblock = (len(args) >= 2 and str(args[-1]).lower() == 'true')
        self.do_left_arm_turn(angle, nonblock)
      
      elif name == 'RA' and len(args) >= 1:
        angle = float(args[0])
        nonblock = (len(args) >= 2 and str(args[-1]).lower() == 'true')
        self.do_right_arm_turn(angle, nonblock)

      elif name == 'AA' and len(args) >= 1:
        if len(args) == 1:
          self.do_arms_turn(float(args[0]))
        else:
          self.do_arms_turn(float(args[0]), float(args[1]))

      elif name == 'W' and len(args) >= 1:
        self.do_wait(float(args[0]))
    self.driveBase.use_gyro(False)
