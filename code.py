import time

import board
import neopixel
from digitalio import DigitalInOut, Pull

from number_generator import NumberGenerator

MIN_BRIGHTNESS = 0.1
MAX_BRIGHTNESS = 1.0

num_pixels = 10
pixels = neopixel.NeoPixel(board.NEOPIXEL, num_pixels, brightness=MIN_BRIGHTNESS, auto_write=False)

button_a = DigitalInOut(board.BUTTON_A)
button_a.switch_to_input(pull=Pull.DOWN)

button_b = DigitalInOut(board.BUTTON_B)
button_b.switch_to_input(pull=Pull.DOWN)


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


def rainbow_cycle(wait):
    brightness = MIN_BRIGHTNESS
    ng = NumberGenerator(0, 256)

    for j in iter(ng):
        initial_a = button_a.value
        initial_b = button_b.value

        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(rc_index & 255)
        pixels.show()

        if not button_a.value and initial_a:
            brightness = brightness_down(brightness)
        if not button_b.value and initial_b:
            brightness = brightness_up(brightness)

        pixels.brightness = brightness
        time.sleep(wait)


while True:
    rainbow_cycle(0)  # Increase the number to slow down the rainbow
