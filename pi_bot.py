# I am a robot

from Adafruit_PWM_Servo_Driver import PWM
from time import sleep
from display import EightByEightPlus
from hd44780 import Hd44780
import smiley
import random
import datetime
import wiringpi2

moods = {
    'happy': {'smiley': smiley.smiley_happy_anim, 'movement': 1, 'action': 'nod'},
    'sad': {'smiley': smiley.smiley_sad_anim, 'movement': 3, 'action': 'shake'},
    'neutral': {'smiley': smiley.smiley_neutral_anim, 'movement': 2, 'action': ''},
    'sleep': {'smiley': smiley.smiley_sleep_anim, 'movement': 0},
    'uhuh': {'smiley': smiley.smiley_uhoh_anim, 'movement': 1, 'action': 'shake'},
    'pacman': {'smiley': smiley.pacman_anim, 'movement': 3, 'action': 'shake nod shake'},
    'ghost': {'smiley': smiley.ghost_anim, 'movement': 3, 'action': 'nod shake nod'},
    'spiral': {'smiley': smiley.spiral_anim, 'movement': 3, 'action': 'dizzy'},
    'grow_spiral': {'smiley': smiley.grow_spiral_anim, 'movement': 3, 'action': 'dizzy dizzy'},
}

SERVO_MIN = 300
SERVO_MAX = 500
PWM_SLEEP = 0.01

INPUT_PINS = {
    'sound-sensor': 1,   # labelled PWM
    'action': 7,  # joystick
    'up': 15,
    'down': 16,
    'left': 10,
    'right': 11,
    }

class PushButtons(object):
    def __init__(self, button_pins):
        self.gpio = wiringpi2.GPIO(wiringpi2.GPIO.WPI_MODE_PINS)
        self.button_pins = button_pins
        self.last_state = {}

        for button_name, button_pin in self.button_pins.items():
            self.gpio.pinMode(button_pin, self.gpio.INPUT)
            self.gpio.pullUpDnControl(button_pin, self.gpio.PUD_UP)

            self.last_state[button_name] = 0  # reset to 0

    def read(self, button_name):
        value = self.gpio.digitalRead(self.button_pins[button_name]) == wiringpi2.GPIO.LOW
        self.last_state[button_name] = value
        return value

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

        self.headx = 0
        self.heady = 0
        self.left_arm_value = 0
        self.right_arm_value = 0
        self.left_foot_value = 0
        self.right_foot_value = 0

        self.mood_list = moods.keys()
        self.mood_idx = 0  # only when using mood_up and mood_down

    def mood(self, mood=None):
        if mood is not None:
            self._mood = mood
            self.lcd.message("  R.O.B.\n%s" % self._mood)
            print 'My mood is %s' % self._mood
        update_grid = self.mood_animations[self._mood].grid_if_update_needed()
        if update_grid is not None:
            self.grid.grid_array(update_grid)
        return self._mood

    def mood_up(self):
        self.mood_idx = (self.mood_idx + 1) % len(self.mood_list)
        self.mood(self.mood_list[self.mood_idx])

    def mood_down(self):
        self.mood_idx = (self.mood_idx - 1) % len(self.mood_list)
        self.mood(self.mood_list[self.mood_idx])

    def mood_arms_and_legs(self):
        self.left_arm(1)
        sleep(.3)
        self.left_arm(0)
        self.right_arm(-1)
        sleep(.3)
        self.right_arm(0)
        self.left_arm(-1)
        sleep(.3)
        self.left_arm(0)
        self.right_arm(1)
        sleep(.3)
        self.right_arm(0)
        self.left_arm(1)
        sleep(.3)
        self.left_arm(0)
        self.right_arm(-1)
        sleep(.3)
        self.right_arm(0)
        self.left_arm(-1)
        sleep(.3)
        self.left_arm(0)
        self.right_arm(1)
        sleep(.3)
        self.right_arm(0)

    def nod(self):
        self.head(0,1)
        sleep(.2)
        self.head(0,-1)
        sleep(.2)
        self.head(0,1)
        sleep(.2)
        self.head(0,-1)
        sleep(.2)
        self.head(0,0)

    def shake(self):
        self.head(1,0)
        sleep(.2)
        self.head(-1,0)
        sleep(.2)
        self.head(1,0)
        sleep(.2)
        self.head(-1,0)
        sleep(.2)
        self.head(0,0)

    def dizzy(self):
        self.head(-1,-1)
        sleep(0.1)
        self.head(1,-1)
        sleep(0.1)
        self.head(1,1)
        sleep(0.1)
        self.head(-1,1)
        sleep(0.1)
        self.head(-1,-1)
        sleep(0.1)
        self.head(1,-1)
        sleep(0.1)
        self.head(1,1)
        sleep(0.1)
        self.head(-1,1)
        sleep(0.1)
        self.head(0,0)

    def head(self, x, y):
        """move head from -1 to 1, (0,0) is center.

        4 is x axis, 
        5 is y axis
        """
        self.headx = x
        self.heady = y
        self.pwm.setPWM(4, 0, int((float(x)+1)/2 * (SERVO_MAX-SERVO_MIN) + SERVO_MIN))
        sleep(PWM_SLEEP)
        self.pwm.setPWM(5, 0, int((float(y)+1)/2 * (SERVO_MAX-SERVO_MIN) + SERVO_MIN))
        sleep(PWM_SLEEP)

    def head_delta(self, delta_x, delta_y):
        self.headx = min(max(self.headx + delta_x, -1), 1)
        self.heady = min(max(self.heady + delta_y, -1), 1)
        self.head(self.headx, self.heady)

    def right_arm(self, value):
        if value == self.right_arm_value:
            return
        self.right_arm_value = value
        self.pwm_360(8, value)

    def left_arm(self, value):
        if value == self.left_arm_value:
            return
        self.left_arm_value = value
        self.pwm_360(10, value)

    def right_foot(self, value):
        if value == self.right_foot_value:
            return
        self.right_foot_value = value
        self.pwm_360(12, value)

    def left_foot(self, value):
        if value == self.left_foot_value:
            return
        self.left_foot_value = value
        self.pwm_360(14, value)

    def pwm_360(self, port, value):
        """Choose a value between -1 and 1"""
        if value == 0:
            self.pwm.setPWM(port, 0, -1)
        else:
            self.pwm.setPWM(port, 0, int(float(value+1) * 0.5 * (453-353) + 353))
        sleep(PWM_SLEEP)

    def reset_pwm(self):
        for i in range(0, 16):
            self.pwm.setPWM(i, 0, -1)
            sleep(PWM_SLEEP)


if __name__ == '__main__':
    # Initialise the PWM device using the default address
    # bmp = PWM(0x40, debug=True)
    pwm = PWM(0x40, debug=True)
    pwm.setPWMFreq(60)                        # Set frequency to 60 Hz

    grid = EightByEightPlus(address=0x71)
    lcd = Hd44780()

    inputs = PushButtons(INPUT_PINS)

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

    me.reset_pwm()
    #import pdb; pdb.set_trace()

    def new_mood(mood):
        # Choose a new mood
        me.mood(mood)
        if 'action' in moods[me._mood]:
            actions = moods[me._mood]['action'].split(' ')
            for action in actions:
                if action == 'nod':
                    me.nod()
                elif action == 'shake':
                    me.shake()
                elif action == 'dizzy':
                    me.dizzy()

        me.head(random.random()-0.5, random.random()-0.5)
        mood_timeout = now + datetime.timedelta(seconds=600.7)
        #me.mood_arms_and_legs()  # will block for a moment

    head_x_target = 0
    head_y_target = 0
    head_x_delta = 0
    head_y_delta = 0

    while 1:
        now = datetime.datetime.now()
        me.mood()  # Triggers update animation
        if head_x_target > me.headx:
            head_x_delta = 0.01
        elif head_x_target < me.headx:
            head_x_delta = -0.01
        else:
            head_x_delta = 0
        if head_y_target > me.heady:
            head_y_delta = 0.01
        elif head_y_target < me.heady:
            head_y_delta = -0.01
        else:
            head_y_delta = 0
        if head_x_delta or head_y_delta:
            me.head_delta(head_x_delta, head_y_delta)

        if now > mood_timeout:
            #new_mood(random.choice(moods.keys()))
            # Choose a new mood
            me.mood(random.choice(moods.keys()))
            #me.head(random.random()-0.5, random.random()-0.5)
            head_x_target = 2 * random.random() - 1
            head_y_target = 2 * random.random() - 1
            mood_timeout = now + datetime.timedelta(seconds=600.7)
            #me.mood_arms_and_legs()  # will block for a moment

        if inputs.read('action'):
            new_right_arm_value = 0
            new_left_arm_value = 0
            new_right_foot_value = 0
            new_left_foot_value = 0
            head_x_target = random.random() - 0.5
            head_y_target = random.random() - 0.5
            if not inputs.last_state['up'] and inputs.read('up'):  # trigger once
                me.mood_up()
                me.nod()
            if not inputs.last_state['down'] and inputs.read('down'):  # trigger once
                me.mood_down()
                me.shake()
            if inputs.read('left'):
                new_left_arm_value = 1
                new_right_arm_value = 1
                new_right_foot_value = 1                
            if inputs.read('right'):
                new_left_arm_value = -1
                new_right_arm_value = -1
                new_left_foot_value = -1
            me.left_arm(new_left_arm_value)
            me.right_arm(new_right_arm_value)
            me.left_foot(new_left_foot_value)
            me.right_foot(new_right_foot_value)
            #if new_left_arm_value == 0 and new_right_arm_value == 0:
            #    # action button only
            #    new_mood(random.choice(moods.keys()))
        else:
            i_moved = False
            if inputs.read('up'):
                me.head_delta(0, -0.1)
                i_moved = True
            if inputs.read('down'):
                me.head_delta(0, 0.1)
                i_moved = True
            if inputs.read('left'):
                me.head_delta(0.1, 0)
                i_moved = True
            if inputs.read('right'):
                me.head_delta(-0.1, 0)
                i_moved = True
            if i_moved:
                head_x_target = me.headx
                head_y_target = me.heady

        sleep(0.01)