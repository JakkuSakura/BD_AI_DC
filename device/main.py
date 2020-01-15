import time
import ssd1306
import machine
import dhtx


Fire = machine.ADC(machine.Pin(36))
Light = machine.ADC(machine.Pin(35))
Hot = machine.ADC(machine.Pin(39))
Water = machine.ADC(machine.Pin(34))
Fire.atten(machine.ADC.ATTN_11DB)
Light.atten(machine.ADC.ATTN_11DB)
Hot.atten(machine.ADC.ATTN_11DB)
Water.atten(machine.ADC.ATTN_11DB)
i2c = machine.I2C(scl = machine.Pin(14), sda = machine.Pin(15), freq = 100000)
oled = ssd1306.SSD1306_I2C(128,64,i2c)
while True:
    F = Fire.read()
    L = Light.read()
    H = Hot.read()
    Deep = Water.read()
    Temp = dhtx.get_dht_temperature('dht11', 5)
    Humi = dhtx.get_dht_relative_humidity('dht11', 5)
    oled.show_fill(0)
    oled.show_str("ID","Temperature:" + str(Temp),"Humidity:" + str(Humi),"Deep:" + str(Deep))
    time.sleep_ms(1000)