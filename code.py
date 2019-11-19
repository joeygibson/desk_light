import time

import adafruit_logging as logging
import board
import neopixel
from digitalio import DigitalInOut, Direction, Pull

from number_generator import NumberGenerator

MIN_BRIGHTNESS = 0.1
MAX_BRIGHTNESS = 1.0

SLOW_SPEED = 5

logger = logging.getLogger('desk_lamp')
logger.setLevel(logging.INFO)

BRIGHTNESS = "brightness"

preferences = {BRIGHTNESS: MAX_BRIGHTNESS}

num_onboard_pixels = 10
num_strip_pixels = 30

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

button_a = DigitalInOut(board.BUTTON_A)
button_a.switch_to_input(pull=Pull.DOWN)

button_b = DigitalInOut(board.BUTTON_B)
button_b.switch_to_input(pull=Pull.DOWN)

switch = DigitalInOut(board.D7)
switch.direction = Direction.INPUT
switch.pull = Pull.UP

onboard_pixels = neopixel.NeoPixel(board.NEOPIXEL, num_onboard_pixels,
                                   brightness=preferences[BRIGHTNESS], auto_write=False)
strip_pixels = neopixel.NeoPixel(board.A1, num_strip_pixels,
                                 brightness=preferences[BRIGHTNESS], auto_write=False)


def blink_led(times):
    for i in range(times):
        led.value = True
        time.sleep(0.1)
        led.value = False
        time.sleep(0.1)


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


def christmas_wheel(pos):
    if pos < 85:
        return 255, 0, 0
    if pos < 170:
        return 0, 255, 0
    else:
        return 255, 215, 0


def brightness_down(brightness_value):
    if brightness_value > MIN_BRIGHTNESS:
        brightness_value -= 0.1

    return brightness_value


def brightness_up(brightness_value):
    if brightness_value < MAX_BRIGHTNESS:
        brightness_value += 0.1

    return brightness_value


def apply_brightness(pixels, brightness_value):
    pixels.brightness = preferences[BRIGHTNESS]


def update_pixels(pixels, iteration, pixel_count):
    for i in range(pixel_count):
        rc_index = (i * 256 // num_onboard_pixels) + iteration

        if switch.value:
            pixels[i] = wheel(rc_index & 255)
        else:
            pixels[i] = christmas_wheel(rc_index & 255)

    pixels.show()


def rainbow_cycle():
    global preferences
    ng = NumberGenerator(0, 256)

    for j in iter(ng):
        initial_a = button_a.value
        initial_b = button_b.value

        update_pixels(onboard_pixels, j, num_onboard_pixels)
        update_pixels(strip_pixels, j, num_strip_pixels)

        if not button_a.value and initial_a:
            preferences[BRIGHTNESS] = brightness_down(preferences[BRIGHTNESS])

        if not button_b.value and initial_b:
            preferences[BRIGHTNESS] = brightness_up(preferences[BRIGHTNESS])

        apply_brightness(onboard_pixels, preferences[BRIGHTNESS])
        apply_brightness(strip_pixels, preferences[BRIGHTNESS])


while True:
    rainbow_cycle()
