# This file is for micropython
try:
    import urequests as requests
    import machine
except:
    import requests
    import random

import json
import device.control_package


class DeviceStatusReporter:
    def get_id(self):
        if 'machine_id' not in self.__dict__:
            try:
                machine_id = machine.unique_id()
                return '{:02x}{:02x}{:02x}{:02x}'.format(machine_id[0], machine_id[1], machine_id[2], machine_id[3])
            except:
                machine_id = random.random()
            self.machine_id = str(machine_id)
        return str(self.machine_id)

    def __init__(self, sever):
        # print('init', id(self))
        self.get_id()
        # self.desp = desp
        self.sever = sever

    def send(self, fire='', water='', temperature='', humidity='', illumination='', flame=''):
        dct = {'machine_id': self.machine_id,
               'fire': fire,
               'water': water,
               'temperature': temperature,
               'humidity': humidity,
               'illumination': illumination,
               'flame': flame
               }
        requests.post("http://" + self.sever + "/device_data",
                      data=json.dumps(dct))

    def send_async(self, *args, **kwargs):
        import _thread
        _thread.start_new_thread(self.send, (*args, *kwargs))

    def get_control(self):
        # return device.control_package.ControlPackage.from_dict(json.loads(requests.post("http://" + self.sever + "/device_request")))
        # fixme
        return None
