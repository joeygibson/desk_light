import board
from digitalio import DigitalInOut, Direction, Pull
import storage

# switch = DigitalInOut(board.D7)  # For Circuit Playground Express
# switch.direction = Direction.INPUT
# switch.pull = Pull.UP
#
# print("mounting storage: " + str(switch.value))
#
# # If the switch pin is connected to ground CircuitPython can write to the drive
# storage.remount("/", switch.value)
