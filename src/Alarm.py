class Alarm(object):

    def __init__(self, led, buzzer, btn) -> None:
        pass
        # super().__init__()
        # self.state = 0
        # self.msg = ""
        # self.alarmBtn = btn
        # self.alarmLED = led
        # self.alarmBuzzer = buzzer
        # GPIO.setup(led,GPIO.OUT)
        # GPIO.setup(buzzer,GPIO.OUT)
        # GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # GPIO.add_event_detect(btn, GPIO.FALLING,
        # callback=self.reset, bouncetime=100)
        # return

    def reset(self):
        pass
        # self.set_state(state=0, msg="clear")
        # return

    def set_state(self, state, msg=""):
        pass
        # self.msg = msg
        # self.state = state

        # if self.state == 0:
        #     GPIO.output(self.alarmBuzzer, False)
        #     GPIO.output(self.alarmLED, False)

        # elif self.state == 1:
        #     GPIO.output(self.alarmBuzzer, False)
        #     GPIO.output(self.alarmLED, True)

        # elif self.state == 2:
        #     GPIO.output(self.alarmLED, True)
        #     GPIO.output(self.alarmBuzzer, True)
