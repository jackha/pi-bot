# I am a robot

from Adafruit_PWM_Servo_Driver import PWM
from time import sleep
from display import EightByEightPlus
from hd44780 import Hd44780
import smiley
import random
import datetime

moods = {
    'happy': {'smiley': smiley.smiley_happy_anim, 'movement': 1},
    'sad': {'smiley': smiley.smiley_sad_anim, 'movement': 3},
    'neutral': {'smiley': smiley.smiley_neutral_anim, 'movement': 2},
    'sleep': {'smiley': smiley.smiley_sleep_anim, 'movement': 0},
    'uhuh': {'smiley': smiley.smiley_uhoh_anim, 'movement': 1},
    'pacman': {'smiley': smiley.pacman_anim, 'movement': 3},
    'ghost': {'smiley': smiley.ghost_anim, 'movement': 3},
    'spiral': {'smiley': smiley.spiral_anim, 'movement': 3},
    'grow_spiral': {'smiley': smiley.grow_spiral_anim, 'movement': 3},
}

SERVO_MIN = 300
SERVO_MAX = 500


class Animation(object):
    def __init__(self, smiley):
        """ Smiley is an array of frames, see smiley_happy"""
        self.smiley = smiley
        self.nof_frames = len(self.smiley)
        self.index = 0
        self.timeout = datetime.datetime.now()

    def grid_if_update_needed(self):
        now = datetime.datetime.now()
        if now > self.timeout:
            self.index = (self.index + 1) % self.nof_frames
            self.timeout = now + datetime.timedelta(seconds=self.smiley[self.index]['time'])
            return self.smiley[self.index]['smiley']
        return None


class Pibot(object):
    def __init__(self, grid, lcd, pwm):
        self.grid = grid
        self.lcd = lcd
        self.pwm = pwm
        self._mood = None
        # prepare animations for moods
        self.mood_animations = {}
        for mood, value in moods.items():
            self.mood_animations[mood] = Animation(value['smiley'])

    def mood(self, mood=None):
        if mood is not None:
            self._mood = mood
            self.lcd.message("  R.O.B.\n%s" % self._mood)
            print 'My mood is %s' % self._mood
        update_grid = self.mood_animations[self._mood].grid_if_update_needed()
        if update_grid is not None:
            self.grid.grid_array(update_grid)
        return self._mood

    def mood_arms_and_legs(self):
        self.left_arm(1)
        self.right_arm(-1)
        sleep(1)
        self.left_arm(-1)
        self.right_arm(1)
        sleep(1)
        self.left_arm(1)
        self.right_arm(-1)
        sleep(1)
        self.left_arm(-1)
        self.right_arm(1)
        sleep(1)

    def head(self, x, y):
        """move head from -1 to 1, (0,0) is center.

        4 is x axis, 
        5 is y axis
        """
        self.pwm.setPWM(4, 0, int((float(x)+1)/2 * (SERVO_MAX-SERVO_MIN) + SERVO_MIN))
        self.pwm.setPWM(5, 0, int((float(y)+1)/2 * (SERVO_MAX-SERVO_MIN) + SERVO_MIN))

    def right_arm(self, value):
        self.pwm_360(10, value)

    def left_arm(self, value):
        self.pwm_360(12, value)

    def right_foot(self, value):
        self.pwm_360(14, value)

    def left_foow(self, value):
        self.pwm_360(16, value)

    def pwm_360(self, port, value):
        """Choose a value between -1 and 1"""
        self.pwm.setPWM(port, 0, float(value+1) * 0.5 * (453-353) + 353)

    def reset_pwm(self):
        for i in range(0, 6):
            self.pwm.setPWM(i, 0, 0)


if __name__ == '__main__':
    # Initialise the PWM device using the default address
    # bmp = PWM(0x40, debug=True)
    pwm = PWM(0x40, debug=True)
    pwm.setPWMFreq(60)                        # Set frequency to 60 Hz

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

    x, y = 0, 0

    now = datetime.datetime.now()
    movement_timeout = now
    mood_timeout = now

    import pdb; pdb.set_trace()

    while 1:
        now = datetime.datetime.now()
        me.mood()  # Triggers update animation

        if now > movement_timeout and me.mood() != 'sleep':
            #me.head(random.random()-0.5, random.random()-0.5)
            #me.left_arm(int(random.random()*1000))
            #movement_timeout = now + datetime.timedelta(seconds=moods[me.mood()]['movement'])
            pass

        if now > mood_timeout:
            # Choose a new mood
            me.mood(random.choice(moods.keys()))
            mood_timeout = now + datetime.timedelta(seconds=3.7)
            me.mood_arms_and_legs()  # will block for a moment

        sleep(0.1)