# pure data for both server and micropython client
class ControlPackage:
    def __init__(self, beeper, light, motor):
        self.beeper = beeper
        self.light = light
        self.motor = motor
    
    @staticmethod
    def from_dict(dic):
        return ControlPackage(dic['beeper'], dic['light'], dic['motor'])
