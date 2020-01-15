# This file is for server
import time
class DeviceInfo:
    def __init__(self, machine_id):
        self.machine_id = machine_id
        self.data = []
        self.warntime = 0
        self.deprtime = 0
    def get_latest_package(self):
        if len(self.data):
            return self.data[-1]
        return None
    def push_package(self, data):
        data['time'] = time.time()
        self.data.append(data)