import time

import board
import neopixel
from digitalio import DigitalInOut, Direction, Pull
import storage
import adafruit_logging as logging

from number_generator import NumberGenerator

MIN_BRIGHTNESS = 0.1
MAX_BRIGHTNESS = 1.0

BRIGHTNESS = "brightness"

logger = logging.getLogger('desk_lamp')
logger.setLevel(logging.INFO)

preferences = {BRIGHTNESS: MIN_BRIGHTNESS}
preference_converters = {BRIGHTNESS: float}

num_onboard_pixels = 10
num_strip_pixels = 30

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

button_a = DigitalInOut(board.BUTTON_A)
button_a.switch_to_input(pull=Pull.DOWN)

button_b = DigitalInOut(board.BUTTON_B)
button_b.switch_to_input(pull=Pull.DOWN)


def blink_led(times):
    for i in range(times):
        led.value = True
        time.sleep(0.1)
        led.value = False
        time.sleep(0.1)


def write_prefs():
    try:
        with open("/prefs.txt", "w") as file:
            for k, v in preferences.items():
                output = "{k}={v}\n".format(k, str(v))
                file.write(output)

            file.flush()
    except OSError as e:
        blink_led(5)

        logger.error("writing preferences: " + str(e))


def read_prefs():
    global preferences
    try:
        with open("/prefs.txt") as file:
            for line in file:
                if len(line.strip()):
                    k, v = line.strip().split('=')
                    logger.info("preferences[{}] = {}".format(k, v))
                    preferences[k] = preference_converters[k](v)
    except OSError as e:
        logger.error("reading preferences: " + str(e))


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return 0, 0, 0
    if pos < 85:
        return 255 - pos * 3, pos * 3, 0
    if pos < 170:
        pos -= 85
        return 0, 255 - pos * 3, pos * 3
    pos -= 170
    return pos * 3, 0, 255 - pos * 3


def brightness_down(brightness_value):
    if brightness_value > MIN_BRIGHTNESS:
        brightness_value -= 0.1

    return brightness_value


def brightness_up(brightness_value):
    if brightness_value < MAX_BRIGHTNESS:
        brightness_value += 0.1

    return brightness_value


def apply_brightness(brightness_value):
    pixels.brightness = preferences[BRIGHTNESS]
    strip.brightness = preferences[BRIGHTNESS]


def rainbow_cycle(wait):
    global preferences
    ng = NumberGenerator(0, 256)

    for j in iter(ng):
        initial_a = button_a.value
        initial_b = button_b.value

        for i in range(num_onboard_pixels):
            rc_index = (i * 256 // num_onboard_pixels) + j
            pixels[i] = wheel(rc_index & 255)

        pixels.show()

        for i in range(num_strip_pixels):
            rc_index = (i * 256 // num_onboard_pixels) + j
            strip[i] = wheel(rc_index & 255)

        strip.show()

        if not button_a.value and initial_a:
            preferences[BRIGHTNESS] = brightness_down(preferences[BRIGHTNESS])
            apply_brightness(preferences[BRIGHTNESS])
            write_prefs()
        if not button_b.value and initial_b:
            preferences[BRIGHTNESS] = brightness_up(preferences[BRIGHTNESS])
            apply_brightness(preferences[BRIGHTNESS])
            write_prefs()

        time.sleep(wait)


logger.info("reading preferences")
read_prefs()

pixels = neopixel.NeoPixel(board.NEOPIXEL, num_onboard_pixels,
                           brightness=preferences[BRIGHTNESS], auto_write=False)
strip = neopixel.NeoPixel(board.A1, num_strip_pixels,
                          brightness=preferences[BRIGHTNESS], auto_write=False)


while True:
    rainbow_cycle(0)  # Increase the number to slow down the rainbow
