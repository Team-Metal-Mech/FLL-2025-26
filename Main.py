from terra_script import TerraScript
from pybricks.parameters import Button
from pybricks.tools import wait

# ⬇️ run_data 리스트는 upload.sh에서 자동으로 삽입됩니다.
run_data = []

def wait_release(hub):
    center_seen = False
    while True:
        p = hub.buttons.pressed()
        if Button.CENTER in p:
            center_seen = True
        if len(p) == 0:
            break
        wait(20)
    return center_seen


robot = TerraScript()
hub = robot.hub

_v = hub.battery.voltage()
_pct = max(0, min(100, round((_v - 7000) / 1200 * 100)))
print("Battery: {}% ({}mV)".format(_pct, _v))

selected = 0
max_index = len(run_data) - 1

while True:
    hub.system.set_stop_button(None)
    hub.display.number(selected + 1)

    while True:
        p = hub.buttons.pressed()

        if Button.CENTER in p:
            wait_release(hub)
            hub.system.set_stop_button(Button.CENTER)
            break

        elif Button.LEFT in p:
            selected = (selected - 1) % (max_index + 1)
            hub.display.number(selected + 1)
            if wait_release(hub):
                hub.system.set_stop_button(Button.CENTER)
                break

        elif Button.RIGHT in p:
            selected = (selected + 1) % (max_index + 1)
            hub.display.number(selected + 1)
            if wait_release(hub):
                hub.system.set_stop_button(Button.CENTER)
                break

    try:
        robot.execute(run_data[selected])
    except SystemExit:
        robot.driveBase.use_gyro(False)
        robot.stop_all()
    finally:
        hub.system.set_stop_button(None)
    wait(300)
