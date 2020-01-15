# pure data for both server and micropython client
class ControlPackage:
    def __init__(self, beeper, light):
        self.beeper = beeper
        self.light = light
    
    @staticmethod
    def from_dict(dic):
        return ControlPackage(dic['beeper'], dic['light'])
