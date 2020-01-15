def pitch(pin=27, freq=440, tim=0):
    from machine import Pin, PWM
    from utime import sleep_ms
    pwm = PWM(Pin(pin))
    if freq > 0:
        pwm.freq(int(freq))  # set frequency
    else:
        pwm.duty(0)
    if tim > 0:
        #pwm.duty(tim)  # set duty cycle
        sleep_ms(tim)
        pwm.deinit()