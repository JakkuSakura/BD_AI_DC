import mymusic
import time
import ssd1306
import machine
import dhtx
import _thread
import control_package
import device_package
import timer
import miot
import json
Fire = machine.ADC(machine.Pin(36))
Light = machine.ADC(machine.Pin(35))
Hot = machine.ADC(machine.Pin(39))
Water = machine.ADC(machine.Pin(34))
Fire.atten(machine.ADC.ATTN_11DB)
Light.atten(machine.ADC.ATTN_11DB)
Hot.atten(machine.ADC.ATTN_11DB)
Water.atten(machine.ADC.ATTN_11DB)
i2c = machine.I2C(scl=machine.Pin(14), sda=machine.Pin(15), freq=100000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
machine.Pin(32, machine.Pin.IN)
reporter = device_package.DeviceStatusReporter("10.0.0.1:5000")

time_delta = 0


fire = 0
light = 0
hot = 0
deep = 0
temp = 0
humi = 0

oled_line_1 = "ID:" + reporter.get_id()
oled_line_2 = "Temp:" + str(temp)
oled_line_3 = "Humid:" + str(humi)
oled_msg = ''


def refresh_oled():
    oled.show_fill(0)
    oled.show_str(oled_line_1, oled_line_2, oled_line_3, oled_msg)
    pass


def set_oled_msg(msg):
    global oled_msg
    oled_msg = str(msg)
    print(msg)
    refresh_oled()


def set_temp(temp):
    global oled_line_2
    oled_line_2 = "Temp:" + str(temp)


def set_humid(humid):
    global oled_line_3
    oled_line_3 = "Humid:" + str(humid)


queue = []


def read_display_task():
    global fire, light, hot, deep
    fire = Fire.read()
    light = Light.read()
    hot = Hot.read()
    deep = Water.read()

    print("Fire", fire)
    print("Light", light)
    print("Hot", hot)
    print("Deep", deep)
    queue.append(reporter.package(
        fire, deep, temp, humi, light, hot, time_delta))


def read_temp_and_humi():
    global temp, humi
    try:
        temp, humi = dhtx.get_dht_tempandhum('dht11', 32)
        set_temp(temp)
        set_humid(humi)
    except Exception as e:
        if 'err' not in str(oled_line_2):
            set_temp('err ' + str(temp))
        if 'err' not in str(oled_line_3):
            set_humid('err ' + str(humi))
        # temp = humi = 0
        print(e)

    refresh_oled()


def receive_package_task(data):
    try:
        control = control_package.ControlPackage.from_dict(json.loads(data))
        # control = reporter.get_control()
        print("beeper", control.beeper)
        print("light", control.light)
        print("motor", control.motor)
        global beeping
        beeping = control.beeper
        global blink_on
        blink_on = control.light
        if control.motor:
            machine.Pin(16, machine.Pin.OUT)
        else:
            machine.Pin(16, machine.Pin.IN)

    except Exception as e:
        print(e)


def send_package_task():
    global queue
    if len(queue) > 3:
        mqueue = queue
        queue = []
        try:
            set_oled_msg("Sending {}".format(len(mqueue)))
            result = reporter.send(mqueue)
            set_oled_msg("Sent:{},st:{}".format(
                len(mqueue), result.status_code))
            mqueue.clear()

            receive_package_task(result.text)

        except Exception as e:
            set_oled_msg("Err wl sdg " + str(e))
            t = queue
            queue = mqueue
            queue.extend(t)


RGB = [machine.Pin(x, machine.Pin.OUT) for x in [0]]  # 0, 2, 4
blink_on = False


def blink():
    while True:
        if blink_on:
            for e in RGB:
                e.value(1 - e.value())
        else:
            for e in RGB:
                e.value(0)
        time.sleep(0.1)


beeping = False


def beep():
    while True:
        if beeping:
            mymusic.pitch(13, 440, 1000)
        else:
            mymusic.pitch(13, -1, 1000)


def networking_thread():
    time.sleep(1)
    timer2 = timer.Timer()
    timer2.push(send_package_task, (), 1)
    timer2.push(read_temp_and_humi, (), 3)

    while True:
        timer2.check_round()
        time.sleep(0.01)


def loop_thread():
    timer1 = timer.Timer()
    timer1.push(read_display_task, (), 1)
    while True:
        timer1.check_round()
        time.sleep(0.01)


if __name__ == "__main__":
    set_oled_msg('Connecting')
    miot.do_connect("JackLaptop", "12345678")
    # miot.do_connect("Jiangkun", "87654321")
    # miot.do_connect("hhhhh", "cdy20011201")
    # miot.do_connect("YourLaptop", "12345678")

    set_oled_msg('Connected')
    t1 = time.time()
    re = reporter.get_clock()
    mid = int(round(float(re.text)))
    t2 = time.time()
    time_delta = mid - (t1 + t2) // 2
    set_oled_msg('Ping code ' + str(re.status_code))

    _thread.start_new_thread(networking_thread, ())
    _thread.start_new_thread(blink, ())
    _thread.start_new_thread(beep, ())
    loop_thread()
