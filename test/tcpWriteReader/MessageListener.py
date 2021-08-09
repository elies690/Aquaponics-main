import csv
from datetime import date,datetime
import asyncio

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

        if tag == "alarm":
            self.system_controller.alarm.set_state(int(data[0]),data[1])
            row = [datetime.now(),data[0],data[1]]
            self._ExcleWrite(row,tag)

        elif tag == "level":
            nb = int(data[0])
            state = int(data[1])
            self.system_controller.level_manager(nb,state)

        elif tag == "pump":
            asyncio.ensure_future(self.system_controller.pumps_manager(data[0]))

    def _ExcelWrite(self,data,tag):
        csv_filename = '/home/pi/Aquaponics/Data/'+str(date.today())+'/'+tag+'.csv'
        with open(csv_filename, 'a') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            csvwriter.writerow(data)
