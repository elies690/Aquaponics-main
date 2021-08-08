import csv
from datetime import date,datetime
class MessageReceivedListener():

    def __init__(self,system_controller):
        self.system_controller = system_controller
        
    def OnMessageReceived(self, message):
        if message == '':
            pass
        else:
            self._handleMessage(message)

    def _handleMessage(self,message):
        msg = message.split(";")
        tag = msg[0]
        data = msg[1:-1]
        print(message)

        if tag == "warning":
            tag = data[0]
            msg = data[1]
            self.system_controller.warnings_manager(tag,msg)
            
        elif tag == "level":
            nb = int(data[0])
            state = int(data[1])
            self.system_controller.level_manager(nb,state)

        elif tag == "pumps":
            active_pump = data[0]
            SWITCH = int(data[1])
            self.system_controller.pumps_manager(active_pump,SWITCH)

        elif tag == 'sensors':
            temp = float(data[0])
            tds = float(data[1])
            self.system_controller.sensors_manager(temp,tds)
            
            
