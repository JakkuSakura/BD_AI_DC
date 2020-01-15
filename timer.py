import time
class Timer:
    def __init__(self):
        self.schedule = []
    def push(self, func, args, interval):
        self.schedule.append(Schedule(func, args, interval))
    def check_round(self):
        for e in self.schedule:
            e.check_and_run()

class Schedule:
    def __init__(self, func, args, interval):
        self.func = func
        self.args = args
        self.interval = interval
        self.last_time = time.time()
    
    def check_and_run(self):
        now = time.time()
        if now - self.last_time > self.interval:
            self.func(*self.args)
            self.last_time = now