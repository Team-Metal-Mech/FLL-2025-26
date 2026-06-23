from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Button, Direction, Port, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait


WHEEL_DIAMETER_MM = 62
AXLE_TRACK_MM = 149
# 팔 모터 대기 제한 시간(ms): 설정 시에만 사용됨
ARM_TIMEOUT_MS = 3000
# 기본 속도/가속도 값(직접 단위 사용)
DEFAULT_STRAIGHT_SPEED = 150   # mm/s
DEFAULT_STRAIGHT_ACCEL = 300   # mm/s^2
DEFAULT_TURN_RATE = 150        # deg/s
DEFAULT_TURN_ACCEL = 180       # deg/s^2
DEFAULT_ARM_SPEED = 200        # deg/s
COLOR_ALIGN_SPEED = 120        # mm/s — 라인 정렬 전용 고정 속도

class TerraScript:
  def __init__(self):
    self.hub = PrimeHub()
    self.left = Motor(Port.E, Direction.COUNTERCLOCKWISE)
    self.right = Motor(Port.F)
    self.driveBase = DriveBase(self.left, self.right, WHEEL_DIAMETER_MM, AXLE_TRACK_MM)
    self.at_left_motor = Motor(Port.C)
    self.at_right_motor = Motor(Port.D)
    # 좌/우 라인트레이스 센서(기본 포트 A, B)
    self.left_color = ColorSensor(Port.A)
    self.right_color = ColorSensor(Port.B)
    self.turn_speed = 200
    self.straight_speed = DEFAULT_STRAIGHT_SPEED
    self.arm_speed = DEFAULT_ARM_SPEED
    self.stop_requested = False
    self.arm_timeout_ms = None
    # 기본 설정 적용
    self.driveBase.settings(straight_speed=DEFAULT_STRAIGHT_SPEED,
                     straight_acceleration=DEFAULT_STRAIGHT_ACCEL,
                     turn_rate=DEFAULT_TURN_RATE,
                     turn_acceleration=DEFAULT_TURN_ACCEL)

  def set_straight_speed(self, value):
    self.straight_speed = int(value)
    self.driveBase.settings(straight_speed=self.straight_speed)

  def set_turn_speed(self, value):
    self.driveBase.settings(turn_rate=int(value))
    self.turn_speed = int(value)
  
  def set_acceleration_speed(self, value):
    self.driveBase.settings(straight_acceleration=int(value),turn_acceleration=int(value))

  def set_arm_speed(self, value):
    self.arm_speed = int(value)
  
  def set_arm_timeout(self, seconds):
    if seconds is None or float(seconds) <= 0:
      self.arm_timeout_ms = None
      return
    self.arm_timeout_ms = int(float(seconds) * 1000)

  def set_straight_acceleration_speed(self, value):
    self.driveBase.settings(straight_acceleration=int(value))

  def set_turn_acceleration_speed(self, value):
    self.driveBase.settings(turn_acceleration=int(value))

  def do_forward(self, value):
    self._drive_distance(round(value * 10))

  def do_backward(self, value):
    self._drive_distance(round(-value * 10))

  def _wait_gyro_settle(self, threshold=1, max_ms=200):
    for _ in range(max_ms // 10):
      h1 = self.hub.imu.heading()
      wait(10)
      h2 = self.hub.imu.heading()
      if abs(h2 - h1) < threshold:
        return

  def do_left_turn(self, value):
    self.driveBase.turn(-value, then=Stop.HOLD)
    self._wait_gyro_settle()

  def do_right_turn(self, value):
    self.driveBase.turn(value, then=Stop.HOLD)
    self._wait_gyro_settle()

  def do_point_right(self, value):
    self.right.run_angle(self.turn_speed, value, then=Stop.HOLD)
    wait(50)

  def do_point_left(self, value):
    self.left.run_angle(self.turn_speed, value, then=Stop.HOLD)
    wait(50)

  def _drive_distance(self, distance_mm):
    if distance_mm == 0:
      return

    if self._check_stop():
      return

    self.driveBase.straight(distance_mm, then=Stop.HOLD)

    if not self.stop_requested:
      wait(50)
  
  def do_left_arm_turn(self, value, nonblock=False):
    self.at_left_motor.run_angle(self.arm_speed, value, then=Stop.HOLD, wait=False)
    if not nonblock:
      self._wait_arm_or_timeout([self.at_left_motor])

  def do_right_arm_turn(self, value, nonblock=False):
    self.at_right_motor.run_angle(self.arm_speed, value, then=Stop.HOLD, wait=False)
    if not nonblock:
      self._wait_arm_or_timeout([self.at_right_motor])

  def do_left_arm_home(self, speed=None, duty_limit=30):
    # 스톨 감지(run_until_stalled)로 하드스톱까지 이동 후 0점 재설정
    # speed 부호로 이동 방향 결정(미지정 시 arm_speed의 반대 방향으로 기본 설정)
    spd = float(speed) if speed is not None else -self.arm_speed
    self.at_left_motor.run_until_stalled(spd, then=Stop.HOLD, duty_limit=int(duty_limit))
    self.at_left_motor.reset_angle(0)
    wait(50)

  def do_right_arm_home(self, speed=None, duty_limit=30):
    spd = float(speed) if speed is not None else -self.arm_speed
    self.at_right_motor.run_until_stalled(spd, then=Stop.HOLD, duty_limit=int(duty_limit))
    self.at_right_motor.reset_angle(0)
    wait(50)

  def do_arms_turn(self, left_value, right_value=None):
    # 양팔을 동시에 회전. 한 값만 주면 두 팔에 동일 적용.
    if right_value is None:
      right_value = left_value

    self.at_left_motor.run_angle(self.arm_speed, left_value, then=Stop.HOLD, wait=False)
    self.at_right_motor.run_angle(self.arm_speed, right_value, then=Stop.HOLD, wait=False)
    self._wait_arm_or_timeout([self.at_left_motor, self.at_right_motor])

  def _wait_arm_or_timeout(self, motors):
    # 타임아웃 미설정 시: 완료될 때까지 대기
    if self.arm_timeout_ms is None:
      while not self._check_stop():
        busy = False
        for motor in motors:
          if not motor.control.done():
            busy = True
            break
        if not busy:
          wait(50)
          return
        wait(50)
      return

    timeout_ms = self.arm_timeout_ms
    elapsed = 0
    slice_ms = 50
    while elapsed < timeout_ms and not self._check_stop():
      busy = False
      for motor in motors:
        if not motor.control.done():
          busy = True
          break
      if not busy:
        wait(50)
        return
      wait(slice_ms)
      elapsed += slice_ms

    # 제한시간 초과 시 모터 정지
    for motor in motors:
      motor.stop()
    wait(50)

  def do_wait(self, value):
    remaining = int(value * 1000)
    slice_ms = 100
    while remaining > 0 and not self._check_stop():
      step = min(slice_ms, remaining)
      wait(step)
      remaining -= step

  def stop_all(self):
    self.driveBase.stop()
    for motor in (self.left, self.right, self.at_left_motor, self.at_right_motor):
      motor.brake()

  def request_stop(self):
    self.stop_requested = True
    self.stop_all()

  def clear_stop_request(self):
    self.stop_requested = False

  def _check_stop(self):
    if self.stop_requested:
      return True
    if Button.CENTER in self.hub.buttons.pressed():
      self.request_stop()
      while Button.CENTER in self.hub.buttons.pressed():
        wait(20)
      return True
    return False

  def gyro_straight(
      self,
      distance_mm,
      speed=None,
      target_heading=None,
      kp=2.0,
      kd=1.5,
      max_turn=180,
      loop_delay_ms=10,
  ):
    if target_heading is None:
      target_heading = self.hub.imu.heading()

    if speed is not None:
      self.set_straight_speed(speed)

    straight_speed = abs(self.straight_speed)
    direction = 1 if distance_mm >= 0 else -1
    target_distance = abs(distance_mm)
    decel_zone = min(150, target_distance * 0.3)
    min_speed = 80
    prev_error = 0

    self.driveBase.reset()

    while abs(self.driveBase.distance()) < target_distance:
      if self._check_stop():
        break
      heading = self.hub.imu.heading()
      error = (target_heading - heading + 180) % 360 - 180

      correction = kp * error + kd * (error - prev_error)
      correction = max(-max_turn, min(max_turn, correction))
      prev_error = error

      remaining = target_distance - abs(self.driveBase.distance())
      if remaining <= decel_zone:
        run_speed = max(min_speed, int(straight_speed * remaining / decel_zone))
      else:
        run_speed = straight_speed

      self.driveBase.drive(direction * run_speed, correction)
      wait(loop_delay_ms)

    self.left.hold()
    self.right.hold()
    wait(50)

  def _is_black(self, sensor, threshold):
    return sensor.reflection() <= threshold

  def color_allign(
      self,
      threshold=15,
      max_forward_mm=600,
      max_align_ms=1500,
      loop_delay_ms=20,
  ):
    approach = self.straight_speed
    align = COLOR_ALIGN_SPEED

    self.driveBase.reset()
    self.driveBase.drive(approach, 0)
    while not self._check_stop():
      left_on = self._is_black(self.left_color, threshold)
      right_on = self._is_black(self.right_color, threshold)
      if left_on or right_on:
        break
      if abs(self.driveBase.distance()) >= max_forward_mm:
        break
      wait(loop_delay_ms)
    self.driveBase.stop()
    wait(30)

    elapsed = 0
    while elapsed < max_align_ms and not self._check_stop():
      left_on = self._is_black(self.left_color, threshold)
      right_on = self._is_black(self.right_color, threshold)
      if left_on and right_on:
        break

      self.left.run(0 if left_on else align)
      self.right.run(0 if right_on else align)

      wait(loop_delay_ms)
      elapsed += loop_delay_ms

    self.left.stop()
    self.right.stop()
    self.driveBase.stop()

  def execute(self, text):
    self.clear_stop_request()
    self.driveBase.stop()
    self.driveBase.settings(
      straight_speed=DEFAULT_STRAIGHT_SPEED,
      straight_acceleration=DEFAULT_STRAIGHT_ACCEL,
      turn_rate=DEFAULT_TURN_RATE,
      turn_acceleration=DEFAULT_TURN_ACCEL,
    )
    self.straight_speed = DEFAULT_STRAIGHT_SPEED
    self.arm_speed = DEFAULT_ARM_SPEED
    self.driveBase.use_gyro(False)
    self._wait_gyro_settle(threshold=0.5, max_ms=2000)
    self.hub.imu.reset_heading(0)
    wait(200)
    self.driveBase.use_gyro(True)
    commands = text.split("#")
    for command in commands:
      if self._check_stop():
        break
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
      
      elif name == 'AT' and len(args) >= 1:
        self.set_arm_timeout(float(args[0]))

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

      elif name == 'LH':
        speed = float(args[0]) if len(args) >= 1 and args[0] else None
        duty = float(args[1]) if len(args) >= 2 and args[1] else 30
        self.do_left_arm_home(speed, duty)

      elif name == 'RH':
        speed = float(args[0]) if len(args) >= 1 and args[0] else None
        duty = float(args[1]) if len(args) >= 2 and args[1] else 30
        self.do_right_arm_home(speed, duty)

      elif name == 'AA' and len(args) >= 1:
        if len(args) == 1:
          self.do_arms_turn(float(args[0]))
        else:
          self.do_arms_turn(float(args[0]), float(args[1]))

      elif name == 'W' and len(args) >= 1:
        self.do_wait(float(args[0]))

      elif name == 'GS' and len(args) >= 1:
        distance_mm = float(args[0])
        speed = float(args[1]) if len(args) >= 2 and args[1] else None

        target_heading = None
        if len(args) >= 3 and args[2]:
          target_heading = float(args[2])

        self.gyro_straight(
          distance_mm,
          speed=speed,
          target_heading=target_heading,
        )
      
      elif name == 'CA':
        threshold = float(args[0]) if len(args) >= 1 and args[0] else 15
        self.color_allign(threshold=threshold)
    self.driveBase.use_gyro(False)
    self.stop_all()
