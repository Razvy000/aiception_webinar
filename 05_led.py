# DONT!!! sudo apt-get install python-rpi.gpio python-gpiozero (will use system python)

# workon aiception
# pip install RPi.GPIO
# pip install gpiozero

import time
from gpiozero import LED

led = LED(7)

led.on()
time.sleep(1)
led.off()


time.sleep(1)

led.on()
time.sleep(1)
led.off()
