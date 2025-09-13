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
  
  def do_left_arm_turn(self, value):
    self.at_left_motor.run_angle(self.arm_speed, value)
    wait(50)
  
  def do_right_arm_turn(self, value):
    self.at_right_motor.run_angle(self.arm_speed, value)
    wait(50)
  
  def do_wait(self, value):
    wait(int(value * 1000))

  def execute(self, text):
    self.driveBase.use_gyro(True)
    commands = text.split("#")
    for command in commands:
      command = command.strip()
      if not command:
        continue
      name, value = command.split(":", 1)
      value = float(value.strip())

      if name == 'SS':  self.set_straight_speed(value)

      elif name == 'ST':  self.set_turn_speed(value)
        
      elif name == 'SA':  self.set_straight_acceleration_speed(value)

      elif name == 'TA':  self.set_turn_acceleration_speed(value)

      elif name == 'AS':  self.set_arm_speed(value)

      elif name == 'F': self.do_forward(value)

      elif name == 'B': self.do_backward(value)

      elif name == 'L': self.do_left_turn(value)

      elif name == 'R': self.do_right_turn(value)

      elif name == 'PR':  self.do_point_right(value) 

      elif name == 'PL':  self.do_point_left(value)

      elif name == 'LA':  self.do_left_arm_turn(value)
      
      elif name == 'RA':  self.do_right_arm_turn(value)

      elif name == 'W': self.do_wait(value)
    self.driveBase.use_gyro(False)