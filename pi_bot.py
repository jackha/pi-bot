# I am a robot

from Adafruit_PWM_Servo_Driver import PWM
from time import sleep
from display import EightByEightPlus
from hd44780 import Hd44780
import smiley

moods = {
    'happy': {'smiley': smiley.smiley},
    'sad': {'smiley': smiley.smiley_cry},
    'pacman': {'smiley': smiley.pacman},
    'ghost': {'smiley': smiley.ghost},
}

SERVO_MIN = 300
SERVO_MAX = 500

class Pibot(object):
    def __init__(self, grid, lcd, pwm):
        self.grid = grid
        self.lcd = lcd
        self.pwm = pwm
        self._mood = None

    def mood(self, mood):
        self._mood = mood
        # TODO: animation
        self.grid.grid_array(moods[mood]['smiley'])
        self.lcd.message("  Pi-bot\n%s" % mood)

    def head(self, x, y):
        """move head from -1 to 1, (0,0) is center.

        4 is x axis, 
        5 is y axis
        """
        self.pwm.setPWM(4, 0, (x+1)/2 * (SERVO_MAX-SERVO_MIN) + SERVO_MIN)
        self.pwm.setPWM(5, 0, (y+1)/2 * (SERVO_MAX-SERVO_MIN) + SERVO_MIN)

if __name__ == '__main__':
    # Initialise the PWM device using the default address
    # bmp = PWM(0x40, debug=True)
    pwm = PWM(0x40, debug=True)
    grid = EightByEightPlus(address=0x71)
    lcd = Hd44780()

    me = Pibot(grid, lcd, pwm)
    me.mood('happy')
    me.head(0,0)
    # Test custom font

    # Write font to CGRAM, there are 8 possible characters to customize. 
    lcd.write4bits(0x40)  # First address.
    for c in [0x0E, 0x1b, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1f]:
        lcd.write4bits(c, True)

    # Now put it on display
    lcd.write4bits(0x80)
    lcd.write4bits(0x00, True)

    while 1:
        import pdb; pdb.set_trace()
        sleep(0.1)