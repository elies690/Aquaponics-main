import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

class Alarm(object):

    def __init__(self, led, buzzer, btn) -> None:
        super().__init__()
        self.state = 0
        self.msg = ""
        self.alarmBtn = btn
        self.alarmLED = led
        self.alarmBuzzer = buzzer
        GPIO.setup(led,GPIO.OUT)
        GPIO.setup(buzzer,GPIO.OUT)
        GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(btn, GPIO.FALLING,
        callback=self.reset, bouncetime=100)
        return

    def reset(self):
        self.set_alarm(state=0, msg="clear")
        return

    def set_state(self, state, msg=""):
        self.msg = msg
        self.state = state

        if self.state == 0:
            GPIO.output(self.alarmBuzzer, False)
            GPIO.output(self.alarmLED, False)
            return

        if self.state == 1:
            GPIO.output(self.alarmBuzzer, False)
            while self.sate:
                GPIO.output(self.alarmLED, True)
                sleep(0.1)
                GPIO.output(self.alarmLED, False)
                sleep(0.1)
            return

        if self.state == 2:
            while self.state:
                GPIO.output(self.alarmLED, True)
                GPIO.output(self.alarmBuzzer, True)
                sleep(0.1)
                GPIO.output(self.alarmLED, False)
                GPIO.output(self.alarmBuzzer, False)
                sleep(0.1)
            return
