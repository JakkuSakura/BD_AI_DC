import time
import device.control_package
import device.device_package
import random
dp = device.device_package.DeviceStatusReporter("127.0.0.1:5000")
dp.machine_id = 'hello'
while True:
    dp.send(random.random() * 60, random.random() * 60, random.random() *
            60, random.random() * 60, random.random() * 60, random.random() * 60)
    time.sleep(3)
