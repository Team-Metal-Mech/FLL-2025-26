from pybricks.parameters import Button
from pybricks.tools import wait

# ⬇️ run_data 리스트는 upload.sh에서 자동으로 삽입됩니다.
run_data = []

def wait_for_button_release(hub):
  while True:
    pressed = hub.buttons.pressed()
    if len(pressed) == 0:
      break
    wait(300)

robot = MetalMechRobot()
hub = robot.hub

selected = 0
max_index = len(run_data) - 1

while True:
    hub.display.number(selected + 1)

    while True:
        p = hub.buttons.pressed()
        if Button.LEFT in p:
            wait_for_button_release(hub)
            break
        elif Button.RIGHT in p:
            selected = (selected + 1) % (max_index + 1)
            hub.display.number(selected + 1)
            wait_for_button_release(hub)

    robot.execute(run_data[selected])
    wait(300)