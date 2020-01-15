import device.device_package
import random
import time
import device_info
import device.control_package
import timer
from device.control_package import ControlPackage

def g(x, y, default=""):
    return x[y] if y in x else default


def gn(x, y, default=0):
    return x[y] if y in x else default


class Monitor:
    def __init__(self):
        self.device_list = []
        self.alive_time = 10  # seconds
        self.warn_time = 60 # seconds
        self.depr_time = 60 # seconds
        self.problematic_device_list = []

    def is_prob(self, package):
        s = bool(g(package, 'fire', False))
        # print(s)
        return s
    def depr_device(self, device):
        device.deprtime = time.time()

    def receive(self, data):
        # print("Received")
        for e in self.device_list:
            if e.machine_id == data['machine_id']:
                e.push_package(data)
                if self.is_prob(data):
                    if e not in self.problematic_device_list:
                        self.problematic_device_list.append(e)
                        e.warntime = time.time()
                elif e in self.problematic_device_list and (time.time() - e.warntime > self.warn_time or time.time() - e.deprtime < self.depr_time):
                    self.problematic_device_list.remove(e)
                break
        else:
            d = device_info.DeviceInfo(data['machine_id'])
            self.device_list.append(d)
            d.push_package(data)
        # print(data)
        # print(len(self.device_list))

    def get_device_info(self, device):
        package = device.get_latest_package()
        info = [device.machine_id, g(package, 'fire'), g(package, 'water'),
                g(package, 'temperature'), g(package, 'humidity'), g(package, 'illumination'), g(package, 'flame'), "Online" if time.time() - package['time'] < self.alive_time else "Offline"]
        return info

    def fetch_device_list(self):
        # Device ID, Desp, fire, water, tempeture, location, alive
        l = []
        for device in self.device_list:
            l.append(self.get_device_info(device))
        return l

    def get_device_by_id(self, machine_id):
        for e in self.device_list:
            if e.machine_id == machine_id:
                return e
        return None

    def calc_control(self, device):
        if time.time() - device.deprtime > self.depr_time and self.is_prob(device.get_latest_package()):
            beeper = True
            light = True
        else:
            beeper = False
            light = False
        return ControlPackage(beeper, light)

    def problematic_devices(self):
        l = []
        for device in self.problematic_device_list:
            l.append(self.get_device_info(device))
        return l
