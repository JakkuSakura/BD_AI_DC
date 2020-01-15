# This file is for micropython
try:
    import urequests as requests
    import machine
except:
    import requests
    import random
import time
import json
try:
    import control_package
except Exception:
    import device.control_package


class DeviceStatusReporter:
    def get_id(self):
        if 'machine_id' not in self.__dict__:
            try:
                machine_id = machine.unique_id()
                return '{:02x}{:02x}{:02x}{:02x}'.format(machine_id[0], machine_id[1], machine_id[2], machine_id[3])
            except:
                machine_id = random.random()
        else:
            return str(self.machine_id)

    def __init__(self, sever):
        # print('init', id(self))
        self.machine_id = self.get_id()
        # self.desp = desp
        self.sever = sever

    def package(self, fire='', water='', temperature='', humidity='', illumination='', flame='', time_delta=0):
        # print('now is', time.time() + time_delta)
        dct = {'machine_id': self.machine_id,
               'fire': fire,
               'water': water,
               'temperature': temperature,
               'humidity': humidity,
               'illumination': illumination,
               'flame': flame,
               'time': time.time() + time_delta
               }
        return dct

    def send(self, lst):
        return requests.post("http://" + self.sever + "/device_data",
                             data=json.dumps(lst))

    def get_clock(self):
        return requests.get('http://' + self.sever + "/clock")

    def get_control(self):
        req = requests.get("http://" + self.sever +
                           "/device_request?id=" + self.machine_id)

        return control_package.ControlPackage.from_dict(json.loads(req.text))
