import requests
import time
import pyclimax as ClimaxApi


def callback(device):
    print('Got callback from device: %s', device.name)

[controller, created] =  ClimaxApi.init_controller('http://127.0.0.1:5000', '', '')

niklas_switch = controller.get_device_by_id('ZB:0000000000006b07')

print(niklas_switch.json_state)

controller.start()

controller.register(niklas_switch, callback)

while 1:
    time.sleep(2)

controller.stop()